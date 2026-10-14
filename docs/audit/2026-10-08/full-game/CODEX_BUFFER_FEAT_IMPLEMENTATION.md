# Eight full feats: actual implementation review

Please independently audit the actual attached candidate guide, reference adapter, adversarial test code and immutable-source evidence. Your first full drafts,15 dependency decisions and five final bridges are incorporated. No feat is promoted; all335 original feat objects are unchanged. The five ordinary spells remain separately reviewed (83/765 catalog) and are not reopened.

Current local checks:131 targeted +2,520 independent healing-budget boundary cases pass. These establish bounded consistency, not numerical balance or a full runtime. All source access, genuine hostile/soul status, geometry, canonical clocks, current item possession, actual damage provenance and actual rest/turn/death/source-root identities are external authoritative host inputs, consistent with earlier packages. Helper certificates do not create those permissions.

Review specifically:
1. Does every printed clause of all eight source objects now have complete, consistent operational text, preserved identity/prerequisite and explicit NEW bridges?
2. Chef: actual ingredient transaction, later PB changes, successful LR finalization, consumption IDs, cross-Chef recipient limit and potency/rest clocks; recipe independence.
3. Inspiring Leader/Blood: snapshots, continuously present selected others, individual vs owner interruption, rejected offers, independent blood save advantage, exact rest ties.
4. Summons/Medic: multi-body lineage versus reissue, actual source costs and shared clocks; dying episode owner identity, real kit use, actual transition before independent background1HP.
5. Necrotic Affinity: unchanged old absorption API, once-actual-turn die, broad personal necrotic fatal-root seal and exact death-instance/rank5 behavior.
6. Lifeleech: zero initial reserve, no level refill, predesignated spell-root/window target, actual damage and anti-farming, two-pass conditional addons, post-reduction finite funding, Critical/excess distinction, no copied/incidental resource-trigger loop.
7. Soul charges/crystal: one owner pool, eligible decline/full-cap body entitlement, ineligible event no rescan, actual sources/souls, crystal transfer no charge transfer, no Soul Bind/whole-soul prestige equivalence.
8. Soul Cage: pay-before-resolution, exact3d8/CONhalf and independent one-family half-heal suppression, refresh/expiry/consumption, self shield and actual fixed DC provider.

If you find a real blocker, identify exact function/paragraph, concrete reproducer and minimal source-consistent correction. Distinguish already declared host responsibilities from defects in the bounded implementation. If the eight full feats are acceptable, explicitly close their authored bounded playtest scope as REVIEWED / reference-VALIDATED, with human balance/whole-world runtime and the remaining327 feats/ordinary Soul Cage spell/Soulrender/recipes separately open. Do not treat old registry provisional-complete flags as review proof.


## Exact file: docs/audit/2026-10-08/full-game/BUFFER_FEAT_COMPLETION_SOURCES.json

```text
{
  "status": "PREPARED / UNDISCUSSED full-clause batch; no feat promotion",
  "scope": "Seven buffer-intersection feats plus the exact Lifeleech dependency of Soul Cage; not the entire335-feat catalog.",
  "sourcePath": "src/data/feats.js",
  "sourceFileSha256": "842d14e868aa93d51fc6f21e39bc9dd3a1b872cdffcf467ffaa99a4cc3f779b6",
  "records": [
    {
      "id": "chef",
      "sourceObject": {
        "id": "chef",
        "name": "Chef",
        "description": "You are an accomplished cook.",
        "prerequisite": "None",
        "effect": "You can cook special food during a long rest that provides temporary hit points to your party.",
        "type": "General",
        "draft": false,
        "deprecated": false,
        "needsReview": false
      },
      "sourceObjectSha256": "0e5b2a5c446a30438540005e0f2bc1754523b0c07f23a3d58d9738758d823de0"
    },
    {
      "id": "inspiring_leader",
      "sourceObject": {
        "id": "inspiring_leader",
        "name": "Inspiring Leader",
        "description": "You can inspire others through stirring words.",
        "prerequisite": "Charisma 13 or higher",
        "effect": "You can spend 10 minutes inspiring your companions, giving them temporary hit points.",
        "type": "General",
        "draft": false,
        "deprecated": false,
        "needsReview": false
      },
      "sourceObjectSha256": "ccf20f2fc5f38ad47473a963c27e49c6cfd5be9d2f2da6b314d71ba583e47d3e"
    },
    {
      "id": "empowered_summoning",
      "sourceObject": {
        "id": "empowered_summoning",
        "name": "Empowered Summoning",
        "description": "A charismatic summoner calls allies with increased health and damage.",
        "prerequisite": "Charisma 14+",
        "effect": "Creatures you summon gain temporary hit points equal to twice your proficiency bonus and add your proficiency bonus to the first damage roll they make each round.",
        "type": "Magic",
        "legacyEffect": "Summoned allies +10% HP and damage",
        "status": "provisional-complete",
        "balanceReview": true,
        "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
        "draft": false,
        "deprecated": false,
        "needsReview": true
      },
      "sourceObjectSha256": "afba301851de043876c6bb7d07d91ea717dd38a05ef6f2609540f0588a6bc31c"
    },
    {
      "id": "field_medic",
      "sourceObject": {
        "id": "field_medic",
        "name": "Field Medic",
        "description": "Trained medical care stabilizes allies faster during combat.",
        "prerequisite": "Trained in Medicine",
        "effect": "You may use a healer’s kit as a bonus action. When you stabilize a creature, it gains temporary hit points equal to your proficiency bonus.",
        "type": "General",
        "legacyEffect": "Stabilize allies in combat faster",
        "status": "provisional-complete",
        "balanceReview": true,
        "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
        "draft": false,
        "deprecated": false,
        "needsReview": true
      },
      "sourceObjectSha256": "e12c23ca62a26cc73da76870d8066b93ea9e29e1518604d0e1e76b354ebc3dab"
    },
    {
      "id": "blood_ritual",
      "sourceObject": {
        "id": "blood_ritual",
        "name": "Blood Ritual",
        "description": "Under the moon's gaze you bind flesh to curse through rites older than the cities of Aethel. Prestige lineage: Mooncursed. completed from the existing development record.)",
        "prerequisite": "Constitution 13+, level 4+",
        "effect": "Once per long rest, as part of a 10-minute ritual using your blood, you gain temporary hit points equal to twice your level and advantage on the next saving throw against curse or disease effects. Required for many lycanthropic oaths. Allies who witness the ritual and share a drop of blood gain half your temporary hit points (rounded down) for 1 hour.",
        "type": "Magic",
        "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
        "legacyEffect": "Once per long rest, as part of a 10-minute ritual using your blood, you gain temporary hit points equal to twice your level and advantage on the next saving throw against curse or disease effects. Required for many lycanthropic oaths. Allies who witness the ritual and share a drop of blood gain half your temporary hit points (rounded down) for 1 hour.",
        "status": "provisional-complete",
        "balanceReview": true,
        "draft": false,
        "deprecated": false,
        "needsReview": true
      },
      "sourceObjectSha256": "5aaa8868de08ed8e614580b12164631975ce589856efeaf5c015ab44505904f7"
    },
    {
      "id": "necrotic_affinity",
      "sourceObject": {
        "id": "necrotic_affinity",
        "name": "Necrotic Affinity",
        "description": "Death's chill is an old friend on Aethel's battlefields—you channel grave-cold through fist and focus without flinching, as if the Binding left a door ajar in your marrow. Prestige lineage: Gravetouched. completed from the existing development record.)",
        "prerequisite": "Proficiency in Religion or level 8+",
        "effect": "You have resistance to necrotic damage. Once per turn when you hit with a melee attack, you can deal an additional 1d6 necrotic damage. When you take necrotic damage from a spell or supernatural effect, you can use your reaction to absorb half of it (rounded down) and add that amount as temporary hit points until the end of your next turn. Creatures you kill with necrotic damage cannot be raised by effects of 5th level or lower for 24 hours.",
        "type": "Magic",
        "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
        "legacyEffect": "You have resistance to necrotic damage. Once per turn when you hit with a melee attack, you can deal an additional 1d6 necrotic damage. When you take necrotic damage from a spell or supernatural effect, you can use your reaction to absorb half of it (rounded down) and add that amount as temporary hit points until the end of your next turn. Creatures you kill with necrotic damage cannot be raised by effects of 5th level or lower for 24 hours.",
        "status": "provisional-complete",
        "balanceReview": true,
        "draft": false,
        "deprecated": false,
        "needsReview": true
      },
      "sourceObjectSha256": "c179a7e4246e9e668e859a699a56179c5ae85fe69d22691d7e9fda1cfe0b23ea"
    },
    {
      "id": "soul_cage",
      "sourceObject": {
        "id": "soul_cage",
        "name": "Soul Cage",
        "description": "You trap the departing in black crystal—voices pressed flat until you need their scream. Prestige lineage: Soulrender. completed from the existing development record.)",
        "prerequisite": "Lifeleech or spellcasting ability, level 8+",
        "effect": "When a hostile creature dies within 30 feet, you may bind its soul to a black crystal, storing up to 3 soul charges. Spend 1 charge to shield an ally for 2d8 temporary HP, or spend 2 charges to fire an Agony Lance (3d8 necrotic, save for half, and the target has disadvantage on the next healing it receives).",
        "type": "Magic",
        "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
        "legacyEffect": "When a hostile creature dies within 30 feet, you may bind its soul to a black crystal, storing up to 3 soul charges. Spend 1 charge to shield an ally for 2d8 temporary HP, or spend 2 charges to fire an Agony Lance (3d8 necrotic, save for half, and the target has disadvantage on the next healing it receives).",
        "status": "provisional-complete",
        "balanceReview": true,
        "draft": false,
        "deprecated": false,
        "needsReview": true
      },
      "sourceObjectSha256": "34a051cc5c242b04c7a7b784acbf69249adc0042ba2a27721ba3433283c9d1fc"
    },
    {
      "id": "lifeleech",
      "sourceObject": {
        "id": "lifeleech",
        "name": "Lifeleech",
        "description": "Your magic does not merely harm—it siphons the vigor that death has not yet claimed. Prestige lineage: Soulrender. completed from the existing development record.)",
        "prerequisite": "Spellcasting ability",
        "effect": "When you deal necrotic damage with a spell, you regain hit points equal to half the necrotic damage dealt. When a hostile creature dies within 30 feet, you absorb a soul spark, gaining 1 soul charge (max 3). Soul charges can power Soul Cage abilities.",
        "type": "Magic",
        "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
        "legacyEffect": "When you deal necrotic damage with a spell, you regain hit points equal to half the necrotic damage dealt. When a hostile creature dies within 30 feet, you absorb a soul spark, gaining 1 soul charge (max 3). Soul charges can power Soul Cage abilities.",
        "status": "provisional-complete",
        "balanceReview": true,
        "draft": false,
        "deprecated": false,
        "needsReview": true
      },
      "sourceObjectSha256": "1ec74c9ea62fd5d8cd1ee136c1589d4b6b752b55adb162c35d54c783321fc932"
    }
  ]
}

```


## Exact file: docs/audit/2026-10-08/full-game/GPT_BUFFER_FEAT_FINAL_BRIDGES.md

```text
# GPT completed five final feat bridges

ChatGPT said:

Chef transaction: accept the proposed bridge. At cooking start, designate 1..current PB intended servings. On successful completion of the cooking work, consume exactly that many real ration-equivalents and create that many physical prepared-food identities. At successful long-rest completion, snapshot current PB and empower min(prepared servings, current PB) of them; each empowered serving grants 2 × current PB temp HP. Any prepared servings above the new PB remain ordinary food. If PB increased, no additional servings appear without ingredients. This is a NEW transaction bridge and preserves the one-batch-per-successful-LR rule.

Lifeleech reserve initialization: confirm uncharged acquisition. Newly acquiring Lifeleech sets RecoveryReserve = 0; no implied rest or free initialization occurs. The next actual completed long rest sets both capacity and current reserve to 2 × current character level. Thereafter level/PB changes between rests do not increase, recompute, or refill it. Persistent characters may load a previously validated reserve/capacity from save state. This is the cleanest finite-resource treatment under the frozen recovery rule.

Lifeleech funding/healing pipeline: confirm, with one precision. Use current Lifeleech reserve during preview so conditional healing add-ons that require positive actual restoration cannot qualify when reserve is 0 or when preview restoration is 0. Apply ordinary healing modifiers/reductions first, then cap the resulting legal funded amount by remaining Lifeleech reserve. On commit, spend the entire funded amount, including any portion that ultimately becomes genuine excess rather than restored HP. Recompute actual HP restoration and excess from that funded amount. Critical's restoration ceiling does not itself turn all funded-but-unrestored healing into excess: genuine excess remains only max(0, funded legal healing − OrdinaryMissingHP). Thus at full HP, funded healing can be genuine excess, but conditional add-ons requiring positive actual HP restoration still do not activate. All lawful healing bonuses draw from the same finite Lifeleech reserve; none creates a second unfunded pool.

Lifeleech child flags: explicit excess converters remain allowed. Interpret noResourceGeneration narrowly as blocking incidental trigger-based resource production caused by the Lifeleech child heal. It does not prohibit a separately authorized excess-healing converter whose exact rule consumes genuine funded excess and outputs RP or another resource. Such a converter must satisfy its own cost/cadence/cap rules, consume each excess point once, and remain subject to any stronger source-specific exclusion. So: blockHealCopyTriggers blocks healing copies; noLifeleechRetrigger blocks recursive Lifeleech; noResourceGeneration blocks incidental resource triggers, but not an explicit legal excess-conversion transaction.

Soul Charge decline: confirm entitlement is spent. An eligible Soul Cage capture opportunity that is voluntarily declined reserves/consumes that owner + body + owner-LR-epoch entitlement exactly like a full-capacity evaluation. A later death of that same body in the same owner LR epoch cannot retry. An actual death checkpoint that fails prerequisites, 30-ft range, perception, line of effect, soul eligibility, or other source legality is recorded as evaluated/ineligible for that death event and cannot be rescanned later after circumstances improve. A later genuinely new death event after resurrection is evaluated fresh, subject to the body/owner epoch restriction. Feat/source ownership, creation lineage, and soul-bearing status remain caller-certified from actual canon; no type-wide soulless assumption is introduced.

```


## Exact file: DescentReviewChanges/ReviewBible/docs/mechanics/BUFFER_FEAT_PLAYTEST.md

```text
# Eight feats: complete candidate rules

**SOURCE-DISCUSSED / RECONCILED CANDIDATE. Independent implementation review pending; no feat promoted.** These rules cover Chef, Inspiring Leader, Empowered Summoning, Field Medic, Blood Ritual, Necrotic Affinity, Lifeleech and the Soul Cage **feat**. They do not authorize the separate Soul Cage spell or complete the other327 feat entries. Numerical balance still needs human playtests.

The335 original feat objects are preserved. Source capture: `docs/audit/2026-10-08/full-game/BUFFER_FEAT_COMPLETION_SOURCES.json` from the game root. Decisions: `GPT_BUFFER_FEAT_FIRST_REVIEW.md`, `GPT_BUFFER_FEAT_BOUNDARIES.md`, `GPT_BUFFER_FEAT_FINAL_BRIDGES.md` in that directory. Later decisions supersede conflicting portions of the first draft. Reference adapter: `tools/buffer_feat_playtest_rules.py`; validation: `tools/validate_buffer_feat_playtests.py`.

## Shared rules

All eight feats are nonrepeatable and require an actual legal feat selection from the character's class progression. There is no extra universal feat schedule. Use the frozen class rules and each class's actual ASI/feat milestones; Oracle and other bespoke schedules retain their exceptions. Check a prerequisite at acquisition. Temporary later loss of an ability-score prerequisite does not revoke the feat; no general retraining rule is created.

“Spellcasting ability” requires a source that actually grants spellcasting and identifies a legal casting ability. Having RP, Revelation Charges or another magical resource is insufficient. A source's statistics do not transfer ownership of another creature's attacks to the statistic provider.

An ally includes the user unless a rule says **other**. Targets must satisfy their source's range, perception, line of effect and creature/living/willing restrictions. A target is counted once through multiple representations. No feature creates a new Action, Bonus Action, Reaction, command or turn unless it says so.

Temporary HP use the world's single grant ledger. Keep only the strongest current grant; an equal offer retains the old grant. Pay legal costs before this comparison. Rejected offers do not refund resources or recipient entitlements. A default-lifetime grant ends at the recipient's next completed long rest, depletion, replacement or applicable dependency ending. Explicit durations replace that default where stated. Temporary HP do not restore normal HP, wake a dying creature, remove Wounds, stabilize it or resurrect it.

Each turn/round/rest/death/physical body/food item/source activation has a persistent canonical identity. Extra Actions are not new turns. A genuine extra turn can satisfy a once-per-turn rule but does not create a new numbered round. Outside initiative use the world's authoritative six-second round-equivalent windows; entering/leaving combat preserves phase and never refreshes an entitlement.

## Chef — General; no prerequisite

During an actual long-rest attempt, use cook's utensils and spend one uninterrupted hour cooking. This is permitted light activity only when the normal long-rest procedure permits that hour; the feat does not enlarge the allowance. Designate one batch of1..current PB intended servings at cooking start. Only one batch may be designated per rest attempt and only one can gain potency per successful completed rest.

On successful cooking completion, consume one real standard ration or meal-equivalent ingredient per intended serving. Create exactly that many physical prepared-food items, each with its own identity. Their food exists immediately, but they gain no feat potency before the rest actually succeeds. If the rest fails, the ingredients remain spent and the food remains ordinary. An incomplete cooking hour creates no special food.

At successful long-rest completion, first resolve old rest-expiring effects and advance the rest epoch. Then snapshot the Chef's current PB and empower up to `min(physically prepared servings still present, current PB)` items. Each grants `2 × PB at batch finalization` temporary HP. A PB increase cannot manufacture more ingredients or servings; a decrease leaves excess prepared items ordinary.

A creature with a legal serving must spend one uninterrupted minute eating it. Completing a legal offer consumes the serving and the recipient's **Chef-family entitlement for its current completed-long-rest epoch**, even if an equal/stronger existing grant wins. This limit is shared across every Chef. The Chef's own rest does not reset another recipient's entitlement.

Potency ends at the earlier of24 elapsed hours from successful batch creation or the Chef's next completed long rest after the creation rest. An already consumed/discarded item never returns. Expired potency leaves ordinary food, with no magical premium value. Potency expiration does not end a previously granted shield; that shield has the recipient's default lifetime.

Chef servings are distinct from crafted Feast recipes. Chef grants no recipe ingredients, crafting checks, RP restoration, creature traits or recipe power. It does not occupy the recipe system's one-feast-at-a-time slot. A lawful recipe rider can coexist with a Chef rider; temporary HP still do not stack. One physical meal cannot claim both effects unless an exact recipe expressly supports it. Recipe-specific ten-minute eating, longer crafting and materials remain independent.

**NEW:** the finite batch transaction, quantities, preparation/eating times, recipient-family cap, potency expiry and explicit no-duplication/economy bridges. The source's long-rest cooking role is preserved.

## Inspiring Leader — General; Charisma13+

Speak for ten uninterrupted minutes. At the start, select up to your current PB **other** willing creatures within30ft. Snapshot your character level and actual signed Charisma modifier then. Each selected creature must remain in range, hear and understand you throughout. No replacements or retargeting during the speech.

On completion, each continuously eligible recipient receives `max(1, snapshotted level + actual CHA modifier)` temporary HP with default lifetime. Each recipient can receive one legal Inspiring-Leader-family offer per its own completed-long-rest epoch, shared across all speakers. An offer rejected by stronger/equal temporary HP still consumes the entitlement.

If one listener loses eligibility, only that listener misses the benefit. If the speaker becomes Incapacitated, cannot continue speaking or abandons the speech, the whole unfinished performance fails. Interrupted speeches spend no recipient entitlements and have no owner per-rest use; the speaker may begin again. Later changes in the speaker's statistics do not change this performance's snapshot. Temporary CHA below13 after acquisition does not disable ownership.

**NEW:** other-creature restriction, count, range/language/presence gates, amount, snapshots and family rest limit.

## Empowered Summoning — Magic; Charisma14+

When your actual source activation genuinely creates a new finite summoned creature, offer it `2 × your PB at creation` temporary HP. Its lifetime is default recipient long rest, also ending when that creature instance ends. Returned/revived preexisting bodies, persistent companion redeploy/rebuild, Mage bound returns, Ranger bonds and devices do not qualify merely by appearing again.

Record a lineage key containing the owner, actual source activation root and creation-slot/body-lineage. Several distinct bodies created by one source each receive their own grant. Reissuing/recreating the same lineage never refreshes its creation grant or its round damage entitlement. A genuinely new activation paid/used under its own rules can create a new root. An Action, limited use, ritual use or item charge can be a real source cost; RP is not mandatory.

Each qualifying creature adds its owner's **current PB** to its first actual damage roll in each canonical round/window. Add this flat bonus once to a shared area roll, not once per affected target. A roll on an ongoing damage tick can qualify; fixed damage without a roll does not consume or receive the rider. Later rolls in that window gain nothing. A critical hit does not double this flat PB bonus.

The creature remains attacker and damage owner. This is not the owner's spell damage. All existing companion command, Bonus Action and offensive budgets remain unchanged. The feat grants neither an initiative entry nor an independent command budget.

**NEW integration:** exact lineage identity, recreation guard and preserved round phase. Creation amount and damage rider are tied to their exact respective PB timings.

## Field Medic — General; trained in Medicine

As a Bonus Action, use one actual healer's-kit use on one legally reachable living dying creature. Resolve the canonical automatic kit stabilization, including its normal1d4-hour recovery deadline. Inventory must contain a real remaining use; this feat invents no kit capacity. This is distinct from the ordinary Action/DC10 Wisdom(Medicine) stabilization option.

Whenever you actually cause a dying→Stable transition by **any legal method**, offer the target your PB temporary HP with default lifetime. Record the transition when it occurs. Already-Stable creatures cannot be stabilized again for a new grant. Record one entitlement per target + actual dying episode + feat owner, plus the actual stabilization event ID. Different owners do not share an artificial family lock, but each must actually cause a valid transition. A new episode requires a genuine exit from the old dying episode and later entry into dying; damage absorbed entirely by temporary HP does not create one.

If you also possess Battlefield Medic's separately sourced Trauma Response, first record the actual kit stabilization, then resolve that background's independent1HP recovery, then resolve Field Medic's temporary-HP offer. The later1HP does not erase the stabilization trigger. The feat itself provides no normal HP, consciousness, Wound removal or resurrection. No background is granted by acquiring this feat.

**NEW integration:** event/episode anti-replay identity and ordering with independent recovery; the broad “when you stabilize” trigger is preserved.

## Blood Ritual — Magic; Constitution13+ and character level4+

Perform a ten-minute ritual once per completed long rest. Commit the use at ritual start. Snapshot your character level, PB and selected targets then: yourself plus up to PB **other** willing allies. Each ally must remain within10ft throughout, witness the ritual and voluntarily contribute a drop of blood. There is no normal-HP payment. No substitutions are allowed after starting.

At completion, offer yourself `2 × snapshotted character level` temporary HP with default lifetime. Each continuously eligible selected ally receives `snapshotted character level` temporary HP for one elapsed hour. A departed/ineligible ally loses only its own benefit. Your interruption fails the whole unfinished ritual and the use remains spent until a real rest resets it.

You also gain advantage on your next actual saving throw against an effect explicitly classified as a curse or disease. This rider is independent of the shield: rejection, replacement or depletion of temporary HP does not remove it. It ends when you roll that qualifying save or complete your next long rest, whichever is first. Consume it on the roll even if advantage cancels disadvantage or the save fails. It neither cures nor waives Oracle's intrinsic Curse and grants no oath or transformation.

If completion is strictly before a long-rest endpoint, the self shield/rider expire at that rest normally. At an exact tied completion, resolve old rest expirations, advance the epoch/reset resources, finalize Chef if applicable, then complete the tied ritual; its new shield/rider belong to the new epoch. Its already-committed start use is never retroactively refunded.

**NEW:** PB ally cap, presence/willingness details, use timing and independent save-rider deadline. Self/ally amounts and the ally's hour follow the reconciled source.

## Necrotic Affinity — Magic; Religion proficiency **or** character level8+

You have resistance to necrotic damage. Once per actual turn, when you hit with a melee attack, you may add1d6 necrotic damage. Natural/form melee attacks and off-turn Reaction attacks can qualify. A critical hit doubles this die to2d6; extra Actions in the same turn do not refresh it, while a genuinely different extra turn has its own entitlement. The die is feat damage, not spell damage.

Preserve the previously reviewed absorption procedure: when a legal necrotic spell/supernatural packet reaches the post-passive-defense stage, you may pay your Reaction to prevent `floor(post-defense necrotic damage /2)` before the old temporary-HP buffer. Resolve the remaining canonical damage once. Afterwards, if the holder remains living, offer temporary HP equal to the prevented amount until the end of the holder's next original regular turn, using its real endpoint marker. A1-point packet spends the Reaction but prevents/grants0. New temporary HP cannot absorb that same packet. Use `BufferLedger.necrotic_affinity` and `finish_necrotic_affinity`; do not apply resistance or damage twice.

When a creature actually dies from a canonical fatal damage/death root containing positive qualifying necrotic harm **owned by you**, attach a Necrotic Affinity seal to that death instance for24 elapsed hours. This includes your spells, the feat die, Agony Lance or another genuinely personal necrotic source. It is not limited to the feat's1d6. Supplying a summoned/transformed creature's statistics does not make its damage yours.

A mixed-type fatal root qualifies if your positive resolved necrotic component belongs to that root and the root actually causes death; no counterfactual subtraction test. Direct Instant Death, fatal death failures at0HP, or a later consequence expressly preserving that necrotic causal root can qualify. Temporary-HP-only absorption with no harmful consequence does not establish a seal.

The seal blocks applicable resurrection with an **actual spellRank/effectiveRank0..5**. Never invent a rank for unranked class features. Reviewed Paladin Grace Reversal is rank5 and is blocked; ordinary Resurrection7 and True Resurrection9 are above this restriction. Other resurrection requirements and Soul Bind still apply independently.

Same owner/death instance does not duplicate; different owners can have separate endpoints, but boolean blocking does not compound. A seal ends by elapsed expiry or an exact source able to remove that blocker, not generic cure. A legal return to life closes that death instance; its historical seals do not persist onto a later death. Transformations never create a new soul/body identity to evade a seal.

**NEW integration:** actual-turn identity, rank translation and fatal-root/death-instance bookkeeping. The broader printed necrotic-kill scope is preserved, correcting the narrower first draft.

## Lifeleech — Magic; actual spellcasting ability

Before your spell's damage resolves, designate one eligible hostile target for that spell root and canonical round/window. Your first positive actual necrotic damage to that target in the window commits the entitlement, even if the eventual healing is0, prohibited, capped or unfunded. No retargeting after observing results; area spells do not harvest a separate heal from every target. The same continuing spell can qualify again in a later real round/window.

Raw self-healing is `floor(actual necrotic damage dealt /2)`. Use only the actual necrotic component, including actual temporary-HP absorption and normal HP lost under the existing actual-damage interface; no overkill. Targets must be genuine hostile opposition, not friendly/staged/trivial sacrifices or owner/ally-generated farming bodies. Natural attacks, Agony Lance and the Necrotic Affinity die alone are not spells. The feat removes no Wounds and cannot resurrect its dead owner.

**NEW finite resource — Lifeleech Recovery Reserve:** newly acquiring the feat starts at0. At each actual completed long rest set its capacity and remaining points to `2 × current character level`, snapshotted then. Level/PB changes between rests do not refill/recompute it. This reserve is neither RP nor Mutation Recovery Reserve. Persistent save imports must preserve validated spent state.

Run the ordinary two-pass healing modifiers/reductions/prohibitions. Preview uses available reserve to determine whether conditional bonuses requiring positive actual HP restoration qualify. Apply reductions before funding. Cap final legal healing potential by remaining reserve; spend that **entire funded amount** on commitment, including funded excess. All lawful healing bonuses consume this same reserve. Then restore HP subject to ordinary maximum HP and Critical ceiling, and calculate `genuine excess = max(0, funded amount − ordinary missing HP)`.

A broad HP-gain prohibition produces0 legal amount, spends0 reserve and creates0 excess. At reserve0 the round/root trigger still commits, but it produces neither restoration nor excess. Full HP can produce funded excess, but does not enable conditional bonuses requiring actual HP restoration. Critical's ceiling does not itself turn all unrestored points into excess.

Lifeleech provides no intrinsic excess converter. A separately authorized converter must have its own eligibility/cost/cadence/cap and consume each funded excess point once. An explicitly legal resource-output converter remains possible; incidental heal-triggered resource production is blocked. The child heal carries `noLifeleechRetrigger`, `blockHealCopyTriggers` and `blockResourceTriggers`; propagate these to downstream callers. The resource flag blocks incidental triggers, not an exact, separately paid excess-conversion transaction. No new resource converter is granted here.

Lifeleech also automatically collects one Soul Charge at an eligible hostile soul-bearing creature's actual death within30ft, perceived with legal line of effect. No crystal is required for Lifeleech's own collection. Use the shared resource/death rules below. Lifeleech alone cannot spend charges through abilities from the unowned Soul Cage feat.

## Soul Cage feat — Magic; level8+ and (Lifeleech **or** actual spellcasting ability)

On acquisition, lock one actually possessed spellcasting source/ability as this feat's DC provider. Agony uses that source's current normal spell-save DC. No freely switchable DC ability or general retraining is created.

**Shared Soul Charges:** each owner has one persistent pool0..3, shared with Lifeleech. A charge is a soul **spark/residue**, not custody of the whole soul. It neither prevents resurrection nor replaces/removes Soul Bind. The ordinary Soul Cage spell is a separate rank6/13RP spell awaiting its own operational review. Soulrender's separate whole-soul ritual unlock still requires actually binding the soul of a living named enemy; residue cannot satisfy it.

At an eligible hostile soul-bearing creature's actual death within30ft, with perception and legal line of effect, Soul Cage permits immediate optional capture with no Action or Reaction. A discrete physical black crystal must actually be possessed and available. Lifeleech collection is automatic and needs no crystal. Owning both never gives two charges for the same death.

Each owner permanently records the exact death event as evaluated, including ineligible events. There is no later corpse rescan after moving closer, gaining a feat/crystal or improving perception. For an eligible event, also reserve the immutable body for that owner's current completed-long-rest epoch. Declining or being at full capacity consumes that entitlement; there is no latent fourth charge. A new real death after resurrection is a new event, but the same body cannot supply the owner again in the same epoch. A future completed rest can permit a future new death, never the old corpse. Different owners evaluate independently.

Created/generated farming bodies and immutable object-origin transformed creatures are ineligible. Soul status otherwise follows actual source/canon or Director adjudication; this feat does not declare every undead/construct category soulless. Death/root/body identities persist through forms.

Charges live on the owner and do not decay automatically. Losing/destroying/transferring the crystal transfers or erases **zero** charges; Soul Cage capture/spending is unavailable without another actual legal black crystal. Another feat owner can use the transferred physical crystal for their own pool. There is no invented price, attunement, HP, durability or crystal charge capacity. During one uninterrupted quiet minute handling the crystal, you may voluntarily dissipate owned charges; this does nothing to any deceased soul.

**Shield:** Bonus Action; pay1 Soul Charge; one legal ally within30ft, including yourself; roll2d8 temporary HP with default lifetime. Pay before strongest-only comparison. An equal/stronger old shield does not refund the charge or Bonus Action.

**Agony Lance:** Action; pay2 Soul Charges; one perceived legal creature within60ft; CON save against the locked provider's current DC. Deal3d8 necrotic damage, half rounded down on success, then ordinary defenses/Core apply once. This is feat damage owned by you, not a spell, RP expenditure or spellcasting trigger.

The target also gains one **Agony healing-suppression family** record until the next committed ordinary HP-healing event with positive pre-reduction potential, or one elapsed minute. That next healing receives an exact×1/2 factor in the canonical healing pipeline. Save success or necrotic immunity affects damage but does not remove this separate rider. Multiple Agony Lances never multiply to1/4: a new paid application refreshes the single endpoint to `max(old expiry, new application+60s)` and retains contributor history.

Consume the suppression on the first applicable committed healing event even if a stronger arithmetic branch wins or actual healing is later capped/prohibited. Suppressed/inapplicable records do not apply or consume; absolute time continues. Temporary HP, stabilization, resurrection, prevention and maximum-HP changes are not ordinary HP healing and do not consume it. Removal requires an exact source capable of removing this magical suppression/debuff; generic cure is insufficient.

**NEW:** prerequisite parsing, residue identity, shared resource/death transaction, conduit role, activations/ranges/DC and the exact healing-suppression conversion. Original source IDs and relationships remain distinct.

## Reference integration and limits

`FeatWorld` takes the actual shared `BufferLedger` and `HealingCommitLedger`. Its rest wrapper processes the shared buffer epoch once; never also process that same rest separately through the buffer ledger. Host scheduler resolves deadlines before new events and supplies true completion timestamps, canonical round/turn IDs and continuous-eligibility records. Mere strings/certificates are not a permission to fabricate elapsed time, line of sight, a new body or a paid summon activation.

Host retains real inventory, geometry, conditions, passive resistance, attacks, saves, damage attribution, class acquisition and current life state. `kit_stabilize` returns the new canonical life state; then record any independent background healing before `finish_stabilization`. `finish_agony` emits one pre-defense damage instruction; caller resolves it once. `drain` returns already-resolved healing: publish its new state once, never heal again. Commit **all** ordinary healing through the shared commit ledger so Agony's one-shot record is consumed once.

Necrotic Affinity's established Reaction helper remains unchanged. General resurrection calls query seals using the exact active death instance and source rank while also checking their other independent soul/body restrictions. Form changes do not reset these histories. Soul Charge acquisition does not alter Soul Bind or whole-soul ownership.

These bounded functions and tests establish rule consistency. They are not a full world scheduler, inventory simulation, campaign economy, soul taxonomy, human balance certification or completion of the separate spell/prestige/recipe systems.

```


## Exact file: DescentReviewChanges/ReviewBible/tools/buffer_feat_playtest_rules.py

```text
"""Eight source-discussed feat candidates; independent implementation review pending.

Use one FeatWorld with the world's canonical BufferLedger and HealingCommitLedger.
The host owns actual acquisition opportunities, geometry, inventory identity,
canonical turn/round/rest events, soul/hostility classification, attack/damage
attribution and all other sources. Certificates below attest those real events;
they are not permissions to invent targets, rounds, deaths or new summon roots.
No function edits the original feat registry or implements a complete game engine.
"""
from dataclasses import dataclass, field, replace
from fractions import Fraction
from core_playtest_rules import stabilize, heal
from form_temphp_playtest_rules import BufferGrant, BufferLedger, require
from healing_playtest_rules import HealingReduction, HealingCommitLedger, healing_packet
from control_playtest_rules import ClockMarker, clock_marker
from spell_playtest_rules import integer, SpellRuleError
from redirection_playtest_rules import identity

FEATS = frozenset(('chef', 'inspiring_leader', 'empowered_summoning', 'field_medic',
                  'blood_ritual', 'necrotic_affinity', 'lifeleech', 'soul_cage'))


@dataclass(frozen=True)
class FeatStats:
    level: int
    pb: int
    charisma_score: int = 10
    charisma_modifier: int = 0
    constitution_score: int = 10
    medicine: bool = False
    religion: bool = False
    # Actual granted casting-source ID -> current normal spell-save DC.
    casting: dict = field(default_factory=dict)

    def __post_init__(self):
        integer(self.level, 'character level', 1, 20)
        integer(self.pb, 'PB', 2, 6)
        for score in (self.charisma_score, self.constitution_score):
            integer(score, 'ability score', 1)
        require(type(self.charisma_modifier) is int, 'Use signed actual CHA modifier')
        for source, dc in self.casting.items():
            identity(source); integer(dc, 'actual source spell-save DC', 1)


@dataclass
class Owner:
    stats: FeatStats
    feats: set = field(default_factory=set)
    acquisition_events: set = field(default_factory=set)
    soul_dc_source: str | None = None
    soul_charges: int = 0
    recovery: int = 0
    recovery_capacity: int = 0
    last_rest: int = 0


@dataclass
class LongActivity:
    id: str
    owner: str
    feat: str
    started: Fraction
    ends: Fraction
    targets: tuple
    level: int
    pb: int
    charisma: int
    state: str = 'active'


@dataclass
class Kit:
    item_id: str
    uses: int

    def __post_init__(self):
        identity(self.item_id); integer(self.uses, 'actual recorded kit uses', 0)


@dataclass
class Rations:
    inventory_id: str
    servings: int

    def __post_init__(self):
        identity(self.inventory_id); integer(self.servings, 'actual ration equivalents', 0)


@dataclass(frozen=True)
class Stabilization:
    event_id: str
    owner: str
    target: str
    episode: str
    pb: int


class FeatWorld:
    def __init__(self, buffers=None, healing_commits=None):
        self.buffers = buffers if buffers is not None else BufferLedger()
        self.healing_commits = healing_commits if healing_commits is not None else HealingCommitLedger()
        self.owners = {}
        self.activities = {}
        self.family_uses = set()
        self.blood_uses = set()
        self.blood_advantage = {}
        self.summon_lineages = {}
        self.summon_damage = set()
        self.stabilizations = {}
        self.stabilization_episodes = set()
        self.finished_stabilizations = set()
        self.melee_turns = set()
        self.seals = {}
        self.ended_deaths = set()
        self.removed_seals = set()
        self.drain_selections = {}
        self.drain_used = set()
        self.soul_events = set()
        self.soul_bodies = set()
        self.spends = {}
        self.agony = {}
        self.agony_generation = 0
        self.chef_attempts = {}
        self.chef_completed = set()
        self.servings = {}

    def register(self, owner, stats):
        identity(owner)
        require(owner not in self.owners and isinstance(stats, FeatStats), 'Register one canonical owner')
        self.owners[owner] = Owner(stats, last_rest=self.epoch(owner))

    def epoch(self, target):
        return self.buffers.rest_epochs.get(target, 0)

    def has(self, owner, feat):
        return owner in self.owners and feat in self.owners[owner].feats

    def require_feat(self, owner, feat):
        require(self.has(owner, feat), 'Actual feat ownership required')
        return self.owners[owner]

    def acquire(self, owner, feat, event_id, *, legal_selection, dc_source=None):
        identity(event_id)
        require(owner in self.owners and feat in FEATS, 'Known owner and feat required')
        o = self.owners[owner]; s = o.stats
        require(legal_selection and event_id not in o.acquisition_events and feat not in o.feats,
                'Actual unspent class feat selection and nonrepeatable feat required')
        gates = {'chef': True, 'inspiring_leader': s.charisma_score >= 13,
                 'empowered_summoning': s.charisma_score >= 14, 'field_medic': s.medicine,
                 'blood_ritual': s.constitution_score >= 13 and s.level >= 4,
                 'necrotic_affinity': s.religion or s.level >= 8,
                 'lifeleech': bool(s.casting),
                 'soul_cage': s.level >= 8 and ('lifeleech' in o.feats or bool(s.casting))}
        require(gates[feat], 'Printed prerequisite not met at acquisition')
        if feat == 'soul_cage':
            require(dc_source in s.casting, 'Lock one actually possessed casting source/ability')
        o.feats.add(feat); o.acquisition_events.add(event_id)
        if feat == 'soul_cage': o.soul_dc_source = dc_source

    def completed_rest(self, owner, epoch):
        """Host calls exactly once for an ACTUAL completed LR, before tie activations.

        This wrapper processes the canonical BufferLedger epoch; do not also call
        BufferLedger.completed_long_rest separately for the same rest.
        """
        self.buffers.completed_long_rest(owner, epoch)
        self.blood_advantage.pop(owner, None)
        if owner in self.owners:
            o = self.owners[owner]; o.last_rest = epoch
            if 'lifeleech' in o.feats:
                o.recovery = o.recovery_capacity = 2 * o.stats.level

    def grant(self, grant_id, feat, owner, target, amount, *, expiry=None, dependencies=()):
        return BufferGrant(grant_id, 'feat:' + feat, owner, target, amount,
                           expiry=expiry, rest_epoch=None if expiry is not None else self.epoch(target),
                           dependencies=dependencies)

    def family_key(self, feat, target):
        return feat, target, self.epoch(target)

    def start_cooking(self, owner, rest_attempt, count, now, *, legal_rest_activity, utensils):
        o = self.require_feat(owner, 'chef'); identity(rest_attempt)
        integer(count, 'intended servings', 1, o.stats.pb)
        key = owner, rest_attempt
        require(key not in self.chef_attempts and legal_rest_activity and utensils,
                'One designated batch per real rest attempt; actual utensils/light-activity allowance required')
        self.chef_attempts[key] = {'count':count, 'start':clock_marker(now).seconds,
                                  'epoch':self.epoch(owner), 'state':'cooking', 'items':[]}

    def finish_cooking(self, owner, rest_attempt, inventory, item_ids, now, *, uninterrupted):
        r = self.chef_attempts[(owner, rest_attempt)]; item_ids = tuple(item_ids)
        require(r['state'] == 'cooking' and uninterrupted and clock_marker(now).seconds >= r['start']+3600,
                'One actual uninterrupted cooking hour required')
        require(inventory.servings >= r['count'] and len(item_ids) == r['count']
                and len(set(item_ids)) == len(item_ids) and not set(item_ids).intersection(self.servings),
                'Pay one real ration equivalent for each unique prepared item')
        for item in item_ids: identity(item)
        inventory.servings -= r['count']; r['state'] = 'prepared'; r['items'] = list(item_ids)
        for item in item_ids:
            self.servings[item] = {'owner':owner, 'state':'ordinary', 'amount':0, 'expiry':None,
                                   'creationEpoch':None}
        return item_ids

    def abort_cooking_rest(self, owner, rest_attempt):
        r = self.chef_attempts[(owner, rest_attempt)]
        require(r['state'] in ('cooking','prepared'), 'Batch already settled')
        r['state'] = 'aborted'  # Already cooked/paid food stays ordinary.

    def finalize_chef(self, owner, rest_attempt, now, *, actual_successful_rest):
        o = self.require_feat(owner, 'chef'); r = self.chef_attempts[(owner, rest_attempt)]
        epoch = self.epoch(owner); key = owner, epoch
        require(actual_successful_rest and r['state'] == 'prepared' and epoch == r['epoch']+1
                and key not in self.chef_completed, 'Finalize one prepared batch just AFTER its actual successful LR')
        items = [i for i in r['items'] if self.servings[i]['state'] == 'ordinary']
        chosen = items[:o.stats.pb]; t = clock_marker(now).seconds
        for item in chosen:
            self.servings[item].update(state='potent', amount=2*o.stats.pb, expiry=t+86400,
                                      creationEpoch=epoch)
        r['state'] = 'finalized'; self.chef_completed.add(key)
        return tuple(chosen)

    def serving_potent(self, item, now):
        s = self.servings[item]
        return (s['state'] == 'potent' and clock_marker(now).seconds < s['expiry']
                and self.epoch(s['owner']) == s['creationEpoch'])

    def consume_chef(self, event_id, item, target, started, now, *, legal_uninterrupted_consumption):
        identity(event_id); identity(target)
        s = self.servings[item]; key = self.family_key('chef', target)
        require(legal_uninterrupted_consumption and clock_marker(now).seconds >= clock_marker(started).seconds+60,
                'Actual legal possession and one uninterrupted minute eating required')
        require(self.serving_potent(item, now) and key not in self.family_uses,
                'Unused potent serving and unused recipient Chef entitlement required')
        g = self.grant(event_id, 'chef', s['owner'], target, s['amount'])
        self.buffers.validate_offer(g, now)
        s['state'] = 'consumed'; self.family_uses.add(key)
        return self.buffers.offer(g, now)

    def retire_serving(self, item, *, actually_consumed_or_discarded):
        require(actually_consumed_or_discarded and self.servings[item]['state'] not in ('consumed','discarded'),
                'Only an actual unconsumed food item can be retired')
        self.servings[item]['state'] = 'discarded'

    def start_activity(self, event_id, owner, feat, targets, now, *, legal):
        o = self.require_feat(owner, feat); identity(event_id)
        require(feat in ('inspiring_leader', 'blood_ritual'), 'Use exact long activation')
        targets = tuple(targets); s = o.stats
        require(legal and event_id not in self.activities, 'Unique legal activation required')
        require(len(set(targets)) == len(targets) and owner not in targets and len(targets) <= s.pb,
                'Select at most PB distinct OTHER recipients at start')
        for target in targets: identity(target)
        if feat == 'inspiring_leader':
            require(all(self.family_key(feat, t) not in self.family_uses for t in targets),
                    'Recipient already received a legal offer this rest')
        else:
            key = owner, self.epoch(owner)
            require(key not in self.blood_uses, 'Blood Ritual already used this rest')
            self.blood_uses.add(key)
        start = clock_marker(now).seconds
        self.activities[event_id] = LongActivity(event_id, owner, feat, start, start+600,
                                                 targets, s.level, s.pb, s.charisma_modifier)
        return self.activities[event_id]

    def interrupt_activity(self, event_id):
        a = self.activities[event_id]
        require(a.state == 'active', 'Activity already settled')
        a.state = 'interrupted'

    def finish_activity(self, event_id, now, *, continuously_eligible):
        """Host tracked each selected recipient throughout; never replace a dropout.

        Owner interruption MUST call interrupt_activity. For exact LR timestamp
        ties host completes the rest first. Offers preflight together before any
        mutation; rejected strongest-only offers still spend family entitlement.
        """
        a = self.activities[event_id]; t = clock_marker(now).seconds
        require(a.state == 'active' and t >= a.ends, 'Actual uninterrupted ten minutes required')
        eligible = set(continuously_eligible)
        require(eligible <= set(a.targets), 'No retargeting during a long activation')
        offers = []
        if a.feat == 'inspiring_leader':
            for target in a.targets:
                if target in eligible and self.family_key(a.feat, target) not in self.family_uses:
                    offers.append(self.grant(a.id+':'+target, a.feat, a.owner, target,
                                             max(1, a.level+a.charisma)))
        else:
            offers.append(self.grant(a.id+':self', a.feat, a.owner, a.owner, 2*a.level))
            for target in a.targets:
                if target in eligible:
                    offers.append(self.grant(a.id+':'+target, a.feat, a.owner, target, a.level,
                                             expiry=ClockMarker(t+3600)))
        for g in offers: self.buffers.validate_offer(g, now)
        a.state = 'completed'
        result = []
        for g in offers:
            if a.feat == 'inspiring_leader': self.family_uses.add(self.family_key(a.feat, g.target))
            result.append(self.buffers.offer(g, now))
        if a.feat == 'blood_ritual': self.blood_advantage[a.owner] = self.epoch(a.owner)
        return result

    def blood_save(self, owner, *, actual_save_rolled, curse_or_disease):
        available = self.blood_advantage.get(owner) == self.epoch(owner)
        if available and actual_save_rolled and curse_or_disease:
            del self.blood_advantage[owner]
            return True
        return False

    def summon_created(self, event_id, owner, source_root, creation_slot, creature, now,
                       *, qualifying_creation, actual_paid_source_activation):
        o = self.require_feat(owner, 'empowered_summoning')
        for value in (event_id, source_root, creation_slot, creature): identity(value)
        require(qualifying_creation and actual_paid_source_activation,
                'Actual finite creature creation by owner, not return/rebuild/device')
        key = owner, source_root, creation_slot
        if key in self.summon_lineages: return None
        g = self.grant(event_id, 'empowered_summoning', owner, creature, 2*o.stats.pb,
                       dependencies=(creature,))
        self.buffers.validate_offer(g, now)
        self.summon_lineages[key] = creature
        return self.buffers.offer(g, now)

    def summon_damage_bonus(self, owner, source_root, creation_slot, round_window, *, actual_damage_roll):
        o = self.require_feat(owner, 'empowered_summoning'); identity(round_window)
        lineage = owner, source_root, creation_slot
        require(lineage in self.summon_lineages, 'Qualifying creation lineage required')
        key = lineage, round_window
        if not actual_damage_roll or key in self.summon_damage: return 0
        self.summon_damage.add(key)
        return o.stats.pb

    def record_stabilization(self, event_id, owner, target, episode, before, after, *, owner_caused):
        o = self.require_feat(owner, 'field_medic')
        for value in (event_id, target, episode): identity(value)
        key = target, episode, owner
        require(owner_caused and not before.dead and before.hp == 0 and not before.stable
                and not after.dead and after.hp == 0 and after.stable,
                'Capture the actual dying-to-Stable transition before later independent healing')
        require(event_id not in self.stabilizations and key not in self.stabilization_episodes,
                'This actual stabilization/owner episode was already recorded')
        record = Stabilization(event_id, owner, target, episode, o.stats.pb)
        self.stabilizations[event_id] = record; self.stabilization_episodes.add(key)
        return record

    def kit_stabilize(self, event_id, owner, target, episode, life, kit, wallet,
                      now, d4, *, legal):
        self.require_feat(owner, 'field_medic')
        require(legal and kit.uses > 0, 'Actual reachable dying target and stocked kit required')
        require(event_id not in self.stabilizations and (target, episode, owner) not in self.stabilization_episodes,
                'Stabilization replay')
        wallet.validate(action='bonus')
        out = replace(life); stabilize(out, d4, now)
        # Validate record identifiers before any resource is spent.
        for value in (event_id, target, episode): identity(value)
        wallet.pay(action='bonus'); kit.uses -= 1
        self.record_stabilization(event_id, owner, target, episode, life, out, owner_caused=True)
        return out

    def finish_stabilization(self, event_id, now, *, living_target):
        r = self.stabilizations[event_id]
        require(event_id not in self.finished_stabilizations, 'Stabilization already finished')
        g = self.grant(event_id+':buffer', 'field_medic', r.owner, r.target, r.pb)
        if living_target: self.buffers.validate_offer(g, now)
        self.finished_stabilizations.add(event_id)
        return self.buffers.offer(g, now) if living_target else None

    def melee_necrotic(self, owner, turn_id, dice, *, melee_hit, opted_in, critical=False):
        self.require_feat(owner, 'necrotic_affinity'); identity(turn_id)
        key = owner, turn_id
        if not (melee_hit and opted_in) or key in self.melee_turns: return 0
        require(len(dice) == (2 if critical else 1), 'One feat d6; two on critical')
        for die in dice: integer(die, 'necrotic d6', 1, 6)
        self.melee_turns.add(key)
        return sum(dice)

    def seal_death(self, owner, death_instance, now, *, actual_dead, owned_necrotic_fatal_root):
        self.require_feat(owner, 'necrotic_affinity'); identity(death_instance)
        require(actual_dead and owned_necrotic_fatal_root and death_instance not in self.ended_deaths,
                'Actual death with positive owned necrotic harm in canonical fatal root required')
        key = owner, death_instance
        if key in self.seals: return False
        self.seals[key] = clock_marker(now).seconds+86400
        return True

    def resurrection_sealed(self, death_instance, now, actual_rank):
        if actual_rank is None or death_instance in self.ended_deaths: return False
        integer(actual_rank, 'actual spell/effective rank', 0)
        if actual_rank > 5: return False
        t = clock_marker(now).seconds
        return any(d == death_instance and t < expiry and (owner, d) not in self.removed_seals
                   for (owner, d), expiry in self.seals.items())

    def remove_seal(self, owner, death_instance, *, explicit_removal):
        require(explicit_removal and (owner, death_instance) in self.seals,
                'Exact source capable of removing this resurrection blocker required')
        self.removed_seals.add((owner, death_instance))

    def returned_to_life(self, death_instance, *, actual_legal_return):
        require(actual_legal_return, 'Only completed legal resurrection ends this death instance')
        self.ended_deaths.add(death_instance)

    def select_drain(self, owner, spell_root, round_window, target, *, eligible_before_damage):
        self.require_feat(owner, 'lifeleech')
        for value in (spell_root, round_window, target): identity(value)
        key = owner, spell_root, round_window
        require(eligible_before_damage and key not in self.drain_selections,
                'Designate one genuine hostile before damage; no retargeting/farming')
        self.drain_selections[key] = target

    def drain(self, event_id, owner, spell_root, round_window, target, life, actual_necrotic_damage,
              *, own_spell_damage, hostile_not_farmed, parent_flags=frozenset(), **healing_options):
        """Commit a finite Lifeleech child heal and return its new canonical life state.

        Damage is the already-resolved necrotic component: actual THP absorption
        plus actual normal HP lost, no overkill. Host uses one canonical six-second
        round-window ID across initiative changes. No copied/Agony/natural-attack
        event may masquerade as owner spell damage. The caller must publish the
        returned state exactly once; no second ordinary healing operation.
        """
        o = self.require_feat(owner, 'lifeleech'); identity(event_id)
        integer(actual_necrotic_damage, 'actual necrotic damage dealt', 0)
        key = owner, spell_root, round_window
        require(self.drain_selections.get(key) == target, 'Use the one target designated before resolution')
        require(own_spell_damage and hostile_not_farmed, 'Actual eligible personal spell damage required')
        require('reserve' not in healing_options, 'The feat owns its one finite reserve')
        if 'noLifeleechRetrigger' in parent_flags or key in self.drain_used or actual_necrotic_damage == 0:
            return None
        if life.dead:
            self.drain_used.add(key)
            return {'state':replace(life), 'fundedAmount':0, 'actualHpGained':0, 'genuineExcess':0,
                    'reserveSpent':0, 'reserveRemaining':o.recovery, 'doesNotResurrect':True}
        packet = healing_packet(life, actual_necrotic_damage//2, reserve=o.recovery, **healing_options)
        funded = min(packet['legalAmount'], o.recovery)
        out = heal(life, funded)
        packet.update(state=out, legalAmount=funded, fundedAmount=funded,
                      preFundingLegalAmount=packet['legalAmount'], actualHpGained=out.hp-life.hp,
                      genuineExcess=max(0, funded-(life.maximum_hp-life.hp)),
                      reserveSpent=funded, reserveRemaining=o.recovery-funded,
                      flags=frozenset(parent_flags)|frozenset(('noLifeleechRetrigger',
                               'blockHealCopyTriggers','blockResourceTriggers')),
                      explicitFundedExcessConversionPermitted=True)
        self.commit_healing(event_id, packet)
        self.drain_used.add(key); o.recovery -= funded
        return packet

    def death_checkpoint(self, owner, event_id, body_id, *, actual_new_death_checkpoint,
                         qualifying_hostile_soul, legal_range_perception_line,
                         crystal_available=False, accept=True):
        """Residue only: no Soul Bind removal, soul custody or resurrection block.

        Even an ineligible checkpoint is permanently evaluated for that owner.
        Eligible decline/full-capacity also reserves that body for the owner LR.
        Canonical immutable body IDs persist through transforms/resurrection.
        """
        require(owner in self.owners and actual_new_death_checkpoint, 'Actual death checkpoint required')
        for value in (event_id, body_id): identity(value)
        event_key = owner, event_id
        require(event_key not in self.soul_events, 'This death event was already evaluated')
        o = self.owners[owner]
        automatic = 'lifeleech' in o.feats
        source = automatic or ('soul_cage' in o.feats and crystal_available)
        eligible = source and qualifying_hostile_soul and legal_range_perception_line
        body_key = owner, body_id, self.epoch(owner)
        self.soul_events.add(event_key)
        if not eligible or body_key in self.soul_bodies: return 0
        self.soul_bodies.add(body_key)
        gained = int(o.soul_charges < 3 and (automatic or accept))
        o.soul_charges += gained
        return gained

    def begin_soul_ability(self, event_id, owner, target, mode, wallet, *, legal, crystal_available):
        o = self.require_feat(owner, 'soul_cage')
        for value in (event_id, target): identity(value)
        require(mode in ('shield', 'agony') and legal and crystal_available,
                'Actual black crystal and source-specific legal creature target required')
        require(event_id not in self.spends, 'Soul ability event replay')
        cost = 1 if mode == 'shield' else 2; action = 'bonus' if mode == 'shield' else 'action'
        require(o.soul_charges >= cost, 'Insufficient actual Soul Charges')
        dc = None
        if mode == 'agony':
            require(o.soul_dc_source in o.stats.casting, 'Locked DC source must supply actual current DC')
            dc = o.stats.casting[o.soul_dc_source]
        wallet.validate(action=action)
        wallet.pay(action=action); o.soul_charges -= cost
        self.spends[event_id] = {'owner':owner, 'target':target, 'mode':mode, 'dc':dc, 'finished':False}
        return {'chargesPaid':cost, 'dc':dc, 'damageOwner':owner, 'sourceKind':'feat'}

    def finish_soul_shield(self, event_id, dice, now):
        p = self.spends[event_id]
        require(p['mode'] == 'shield' and not p['finished'], 'Pending paid shield required')
        require(len(dice) == 2, 'Roll exactly 2d8')
        for die in dice: integer(die, 'shield d8', 1, 8)
        g = self.grant(event_id, 'soul_cage', p['owner'], p['target'], sum(dice))
        self.buffers.validate_offer(g, now)
        p['finished'] = True
        return self.buffers.offer(g, now)

    def finish_agony(self, event_id, dice, now, *, con_save_success):
        """Return the single damage instruction, before defenses/Core resolution.

        The separate healing rider applies regardless of save/immunity; source
        targeting legality was established before payment. Never deal the returned
        damage a second time when committing the caller's canonical damage event.
        """
        p = self.spends[event_id]
        require(p['mode'] == 'agony' and not p['finished'], 'Pending paid Agony Lance required')
        require(len(dice) == 3 and type(con_save_success) is bool, 'Actual CON result and 3d8 required')
        for die in dice: integer(die, 'Agony d8', 1, 8)
        t = clock_marker(now).seconds
        old = self.agony.get(p['target'])
        if old is not None and old['expires'] > t:
            old['expires'] = max(old['expires'], t+60)
            old['owner'] = p['owner']; old['contributors'].append(event_id)
        else:
            self.agony_generation += 1
            self.agony[p['target']] = {'id':'agony-healing:'+str(self.agony_generation),
                 'expires':t+60, 'owner':p['owner'], 'contributors':[event_id]}
        p['finished'] = True
        return {'damage':sum(dice)//2 if con_save_success else sum(dice), 'type':'necrotic',
                'damageOwner':p['owner'], 'sourceKind':'feat', 'spellRoot':None}

    def agony_reduction(self, target, now, *, suppressed=False):
        r = self.agony.get(target)
        if r is None or clock_marker(now).seconds >= r['expires']: return None
        return HealingReduction(r['id'], 'feat:soul_cage:agony', 'factor', Fraction(1,2),
                                suppressed=suppressed, next_healing=True)

    def commit_healing(self, event_id, packet):
        ids = self.healing_commits.commit(event_id, packet)
        self.agony = {t:r for t,r in self.agony.items() if r['id'] not in ids}
        return ids

    def remove_agony(self, target, *, explicit_removal):
        require(explicit_removal, 'Exact removal of magical healing suppression required')
        return self.agony.pop(target, None)

    def release_souls(self, owner, amount, *, actual_quiet_minute, crystal_available):
        o = self.require_feat(owner, 'soul_cage'); integer(amount, 'charges released', 1, 3)
        require(actual_quiet_minute and crystal_available and o.soul_charges >= amount,
                'Actual one-minute crystal handling and owned charges required')
        o.soul_charges -= amount

```


## Exact file: DescentReviewChanges/ReviewBible/tools/validate_buffer_feat_playtests.py

```text
"""Adversarial reference checks for eight full feat candidates; no promotion."""
from dataclasses import replace
from fractions import Fraction
from pathlib import Path
import hashlib
import json
from buffer_feat_playtest_rules import FeatWorld, FeatStats, FEATS, Kit, Rations
from device_lifecycle_playtest_rules import Wallet
from core_playtest_rules import LifeState, heal, stabilize
from form_temphp_playtest_rules import BufferGrant
from healing_playtest_rules import HealingReduction, healing_packet, HealingChain, ExcessLedger
from spell_playtest_rules import SpellRuleError
from control_playtest_rules import ClockMarker, turn_end_deadline

ROOT = Path(__file__).resolve().parents[1]
checks = []
matrix = 0


def check(name, value):
    if not value: raise AssertionError(name)
    checks.append(name)


def rejects(name, function):
    try: function()
    except SpellRuleError: checks.append(name); return
    raise AssertionError('Expected rejection: '+name)


def world(feats=FEATS, owners=('a',), stats=None):
    w = FeatWorld()
    s = stats or FeatStats(8, 3, 14, 2, 14, True, True, {'mage:INT':15})
    for owner in owners:
        w.register(owner, s)
        for feat in sorted(feats):
            w.acquire(owner, feat, owner+':acquire:'+feat, legal_selection=True,
                      dc_source='mage:INT' if feat == 'soul_cage' else None)
    return w


def strong(w, target, amount=99, ident='strong'):
    w.buffers.offer(BufferGrant(ident, 'external', target, target, amount, rest_epoch=w.epoch(target)))


def cooking(w, owner='a', attempt='r1', count=3, now=0):
    inv = Rations('inventory:'+owner, count)
    w.start_cooking(owner, attempt, count, now, legal_rest_activity=True, utensils=True)
    ids = tuple(owner+':'+attempt+':food:'+str(i) for i in range(count))
    w.finish_cooking(owner, attempt, inv, ids, now+3600, uninterrupted=True)
    return inv, ids


def drain(w, event='h1', root='s1', window='round:1', life=None, damage=12, **options):
    w.select_drain('a', root, window, 'foe', eligible_before_damage=True)
    return w.drain(event, 'a', root, window, 'foe', life or LifeState(20,5), damage,
                   own_spell_damage=True, hostile_not_farmed=True, **options)


def death(w, event, body=None, owner='a', **options):
    return w.death_checkpoint(owner, event, body or event, actual_new_death_checkpoint=True,
             qualifying_hostile_soul=options.pop('qualifying_hostile_soul',True),
             legal_range_perception_line=options.pop('legal_range_perception_line',True), **options)


def lance(w, event, target='foe', now=0, success=False, owner='a'):
    w.owners[owner].soul_charges = 2  # Fixture imports an already validated resource balance.
    wallet = Wallet()
    p = w.begin_soul_ability(event, owner, target, 'agony', wallet, legal=True, crystal_available=True)
    return p, w.finish_agony(event,(3,4,6),now,con_save_success=success), wallet


def main():
    global matrix
    w=world()
    check('all eight acquired once', w.owners['a'].feats == FEATS)
    rejects('no repeated feat', lambda:w.acquire('a','chef','again',legal_selection=True))
    poor=world(feats=(),stats=FeatStats(3,2))
    for feat in FEATS-{'chef'}:
        rejects('prerequisite '+feat,lambda f=feat:poor.acquire('a',f,f,legal_selection=True))
    rejects('actual selection required',lambda:poor.acquire('a','chef','fake',legal_selection=False))
    check('acquisition does not grant reserve',w.owners['a'].recovery==0)
    w.completed_rest('a',1)
    check('completed rest fills finite reserve',w.owners['a'].recovery==16)
    rejects('same rest cannot repeat',lambda:w.completed_rest('a',1))
    w.owners['a'].stats=replace(w.owners['a'].stats,level=12,pb=4)
    check('level change is not refill',w.owners['a'].recovery==16 and w.owners['a'].recovery_capacity==16)

    w=world(owners=('a','b'))
    inv,ids=cooking(w)
    check('actual ingredients spent',inv.servings==0)
    check('cooked food has no pre-rest potency',not w.serving_potent(ids[0],4000))
    rejects('unfinished rest cannot empower',lambda:w.finalize_chef('a','r1',4000,actual_successful_rest=False))
    w.owners['a'].stats=replace(w.owners['a'].stats,pb=4)
    w.completed_rest('a',1)
    empowered=w.finalize_chef('a','r1',28800,actual_successful_rest=True)
    check('PB increase never manufactures fourth food',len(empowered)==3)
    check('current PB determines finalized shield',w.servings[ids[0]]['amount']==8)
    rejects('cannot finalize batch twice',lambda:w.finalize_chef('a','r1',28800,actual_successful_rest=True))
    strong(w,'recipient')
    offer=w.consume_chef('eat1',ids[0],'recipient',28800,28860,legal_uninterrupted_consumption=True)
    check('rejected Chef shield still consumes food and entitlement',not offer['accepted'] and w.servings[ids[0]]['state']=='consumed')
    rejects('same recipient second Chef serving',lambda:w.consume_chef('eat2',ids[1],'recipient',28860,28920,legal_uninterrupted_consumption=True))
    rejects('serving identity replay',lambda:w.consume_chef('replay',ids[0],'other',28860,28920,legal_uninterrupted_consumption=True))
    w.completed_rest('recipient',1)
    check('recipient own rest resets family entitlement',w.consume_chef('eat3',ids[1],'recipient',28920,28980,legal_uninterrupted_consumption=True)['accepted'])
    w.completed_rest('a',2)
    check('chef next rest ends unused potency',not w.serving_potent(ids[2],29000))
    check('chef rest does not erase already granted shield',w.buffers.amount('recipient')==8)
    w=world(); inv,ids=cooking(w); w.abort_cooking_rest('a','r1')
    check('failed rest retains ordinary paid food',inv.servings==0 and w.servings[ids[0]]['state']=='ordinary')
    rejects('aborted batch never finalizes',lambda:w.finalize_chef('a','r1',28800,actual_successful_rest=True))
    w=world(); inv,ids=cooking(w); w.owners['a'].stats=replace(w.owners['a'].stats,pb=2)
    w.completed_rest('a',1); chosen=w.finalize_chef('a','r1',28800,actual_successful_rest=True)
    check('PB decrease leaves ordinary remainder',len(chosen)==2 and w.servings[ids[2]]['state']=='ordinary')
    check('exact 24h potency endpoint',w.serving_potent(ids[0],115199) and not w.serving_potent(ids[0],115200))
    rejects('one minute eating required',lambda:w.consume_chef('fast',ids[0],'b',28800,28859,legal_uninterrupted_consumption=True))
    w.retire_serving(ids[1],actually_consumed_or_discarded=True)
    check('discarded item stays unavailable',not w.serving_potent(ids[1],28900))

    w=world(owners=('a','b')); strong(w,'listener')
    w.start_activity('speech','a','inspiring_leader',('listener','left'),0,legal=True)
    w.owners['a'].stats=replace(w.owners['a'].stats,charisma_score=8,charisma_modifier=-1,level=12)
    rejects('speech not completed early',lambda:w.finish_activity('speech',599,continuously_eligible=('listener',)))
    result=w.finish_activity('speech',600,continuously_eligible=('listener',))
    check('speech start snapshot and rejected offer consumption',result[0]['amount']==10 and not result[0]['accepted'])
    check('departing listener alone loses benefit',w.buffers.amount('left')==0)
    rejects('different speaker same recipient cap',lambda:w.start_activity('s2','b','inspiring_leader',('listener',),700,legal=True))
    rejects('speaker cannot target self',lambda:w.start_activity('self','a','inspiring_leader',('a',),700,legal=True))
    w.start_activity('fail','a','inspiring_leader',('new',),700,legal=True); w.interrupt_activity('fail')
    rejects('interrupted speech cannot complete',lambda:w.finish_activity('fail',1300,continuously_eligible=('new',)))
    w.start_activity('restart','a','inspiring_leader',('new',),1300,legal=True)
    check('owned feat survives later CHA loss',w.finish_activity('restart',1900,continuously_eligible=('new',))[0]['amount']==11)
    rejects('completed speech replay',lambda:w.finish_activity('restart',1901,continuously_eligible=('new',)))

    w=world(); strong(w,'a')
    w.start_activity('blood','a','blood_ritual',('ally','left'),0,legal=True)
    rejects('blood use commits at start',lambda:w.start_activity('blood2','a','blood_ritual',(),0,legal=True))
    w.owners['a'].stats=replace(w.owners['a'].stats,level=10)
    result=w.finish_activity('blood',600,continuously_eligible=('ally',))
    check('blood level snapshotted at start',result[0]['amount']==16 and result[1]['amount']==8)
    check('blood ally exact one-hour deadline',w.buffers.current('ally').expiry==ClockMarker(4200))
    check('blood advantage exists despite rejected self shield',w.blood_save('a',actual_save_rolled=False,curse_or_disease=True)==False and 'a' in w.blood_advantage)
    check('unrelated save preserves advantage',not w.blood_save('a',actual_save_rolled=True,curse_or_disease=False) and 'a' in w.blood_advantage)
    check('qualifying actual roll consumes independent rider',w.blood_save('a',actual_save_rolled=True,curse_or_disease=True) and not w.blood_save('a',actual_save_rolled=True,curse_or_disease=True))
    w.completed_rest('a',1);w.start_activity('tie','a','blood_ritual',(),1000,legal=True)
    w.completed_rest('a',2);w.finish_activity('tie',1600,continuously_eligible=())
    check('post-rest tie grant belongs to new epoch',w.buffers.current('a').rest_epoch==2 and w.blood_advantage['a']==2)
    w.completed_rest('a',3);w.start_activity('interrupted','a','blood_ritual',(),2000,legal=True);w.interrupt_activity('interrupted')
    rejects('interrupted ritual still spends use',lambda:w.start_activity('retry','a','blood_ritual',(),3000,legal=True))

    w=world()
    for slot in ('first','second'):
        w.summon_created(slot,'a','root',slot,slot,0,qualifying_creation=True,actual_paid_source_activation=True)
    check('two genuine bodies receive independent creation shields',w.buffers.amount('first')==6 and w.buffers.amount('second')==6)
    w.buffers.end_dependency('first')
    check('ended creature loses grant',w.buffers.amount('first')==0)
    check('same lineage recreation grants nothing',w.summon_created('reissue','a','root','first','new-body',1,qualifying_creation=True,actual_paid_source_activation=True) is None)
    check('fixed damage does not use rider',w.summon_damage_bonus('a','root','first','round:1',actual_damage_roll=False)==0)
    w.owners['a'].stats=replace(w.owners['a'].stats,pb=4)
    check('rolled damage uses current PB',w.summon_damage_bonus('a','root','first','round:1',actual_damage_roll=True)==4)
    check('shared roll/reissue same round cannot duplicate',w.summon_damage_bonus('a','root','first','round:1',actual_damage_roll=True)==0)
    check('other creature own roll entitlement',w.summon_damage_bonus('a','root','second','round:1',actual_damage_roll=True)==4)
    check('next true round qualifies',w.summon_damage_bonus('a','root','first','round:2',actual_damage_roll=True)==4)
    rejects('unpaid root cannot be invented',lambda:w.summon_created('bad','a','fake','slot','body',0,qualifying_creation=True,actual_paid_source_activation=False))
    rejects('device/rebuild ineligible',lambda:w.summon_created('device','a','real','slot','device',0,qualifying_creation=False,actual_paid_source_activation=True))

    w=world(); kit=Kit('kit',1); wallet=Wallet(); dying=LifeState(20,0,death_failures=2)
    stable=w.kit_stabilize('st','a','patient','episode1',dying,kit,wallet,0,2,legal=True)
    check('kit pays one actual use and BA',kit.uses==0 and not wallet.bonus_action)
    check('canonical stabilization no HP and clears failures',stable.stable and stable.hp==0 and stable.death_failures==0 and stable.stable_until_seconds==7200)
    recovered=heal(stable,1)
    check('separate background recovery preserves recorded trigger',recovered.hp==1 and w.finish_stabilization('st',0,living_target=True)['amount']==3)
    rejects('no duplicate stabilization grant',lambda:w.finish_stabilization('st',0,living_target=True))
    rejects('already Stable cannot trigger',lambda:w.record_stabilization('bad','a','patient','episode1',stable,stable,owner_caused=True))
    new_stable=replace(dying);stabilize(new_stable,1,1)
    w.record_stabilization('spell','a','patient','episode2',dying,new_stable,owner_caused=True)
    check('new actual episode / other method qualifies',w.finish_stabilization('spell',1,living_target=True)['amount']==3)
    rejects('empty real kit rejected before action',lambda:w.kit_stabilize('empty','a','p','e',dying,kit,Wallet(),2,1,legal=True))
    check('input LifeState not mutated',not dying.stable and dying.death_failures==2)

    w=world(owners=('a','b'))
    check('optional declined melee rider retains turn',w.melee_necrotic('a','turn1',(),melee_hit=True,opted_in=False)==0)
    check('melee critical doubles feat die',w.melee_necrotic('a','turn1',(3,5),melee_hit=True,opted_in=True,critical=True)==8)
    check('extra Action does not refresh',w.melee_necrotic('a','turn1',(6,),melee_hit=True,opted_in=True)==0)
    check('off-turn hit can qualify',w.melee_necrotic('a','enemy-turn',(4,),melee_hit=True,opted_in=True)==4)
    check('genuine extra turn qualifies',w.melee_necrotic('a','extra-turn',(2,),melee_hit=True,opted_in=True)==2)
    rejects('no seal for nonfatal/THP-only harm',lambda:w.seal_death('a','death',0,actual_dead=False,owned_necrotic_fatal_root=True))
    w.seal_death('a','death',0,actual_dead=True,owned_necrotic_fatal_root=True)
    check('same owner death redundant',not w.seal_death('a','death',1,actual_dead=True,owned_necrotic_fatal_root=True))
    check('rank5 blocked; higher and unknown not inferred',w.resurrection_sealed('death',1,5) and not w.resurrection_sealed('death',1,6) and not w.resurrection_sealed('death',1,None))
    check('24h exact expiry',w.resurrection_sealed('death',86399,0) and not w.resurrection_sealed('death',86400,5))
    w.seal_death('b','death',10,actual_dead=True,owned_necrotic_fatal_root=True)
    w.remove_seal('a','death',explicit_removal=True)
    check('separate owner seal remains',w.resurrection_sealed('death',20,5))
    rejects('generic cure cannot erase seal',lambda:w.remove_seal('b','death',explicit_removal=False))
    w.returned_to_life('death',actual_legal_return=True)
    check('legal return closes exact old death',not w.resurrection_sealed('death',30,5))
    w.seal_death('a','death2',40,actual_dead=True,owned_necrotic_fatal_root=True)
    check('new later death separately sealable',w.resurrection_sealed('death2',40,5))
    w=world(); wallet=Wallet(); life=LifeState(20,20)
    reaction=w.buffers.necrotic_affinity('a','necro',6,wallet,turn_end_deadline(12),legal=True)
    after,ev=w.buffers.core_damage('a','necro',life,reaction['remainingDamage'])
    offer=w.buffers.finish_necrotic_affinity('a','necro','absorbed',0,living_holder=True)
    check('reviewed reaction pipeline preserved',not wallet.reaction and after.hp==17 and reaction['prevented']==3 and offer['amount']==3)

    w=world(); p=drain(w)
    check('uncharged acquisition cannot heal or create excess',p['fundedAmount']==0 and p['actualHpGained']==0 and p['genuineExcess']==0)
    w.completed_rest('a',1)
    check('same root round entitlement remains spent after rest',w.drain('again','a','s1','round:1','foe',LifeState(20,5),12,own_spell_damage=True,hostile_not_farmed=True) is None)
    p=drain(w,event='h2',window='round:2')
    check('actual drain funds finite HP',p['actualHpGained']==6 and p['reserveSpent']==6 and w.owners['a'].recovery==10)
    rejects('no after-the-fact retarget',lambda:w.select_drain('a','s1','round:2','other',eligible_before_damage=True))
    p=drain(w,event='h3',root='s3',life=LifeState(20,20),damage=30,conditional_flat_bonuses=(99,))
    check('full HP finite excess spends remaining budget',p['genuineExcess']==10 and p['reserveSpent']==10 and p['actualHpGained']==0 and not p['conditionalAddonsQualify'])
    check('zero remaining cannot farm extra conversions',drain(w,event='h4',root='s4',life=LifeState(20,20),damage=200)['genuineExcess']==0)
    chain=HealingChain('root')
    check('child healing cannot copy or trigger resource gain',chain.child('copy',kind='copy',parent_flags=p['flags']) is None and chain.child('resource',kind='resource',parent_flags=p['flags']) is None)
    excess=ExcessLedger(p['genuineExcess'],internal_resolved=True)
    check('authorized external conversion gets finite excess',excess.convert(10,kind='temp-hp',source_eligible=True)==10)
    rejects('excess cannot spend twice',lambda:excess.convert(1,kind='damage',source_eligible=True))
    w=world();w.completed_rest('a',1)
    p=drain(w,hp_gain_prohibited=True,damage=100)
    check('prohibition spends no reserve or excess',p['fundedAmount']==0 and p['genuineExcess']==0 and w.owners['a'].recovery==16)
    p=drain(w,event='crit',root='crit',life=LifeState(20,18,wounds=(None,None,None)),damage=4)
    check('Critical ceiling loss is not automatically excess',p['fundedAmount']==2 and p['actualHpGained']==1 and p['genuineExcess']==0)
    w.select_drain('a','zero','round:1','foe',eligible_before_damage=True)
    check('zero actual damage does not commit entitlement',w.drain('zero','a','zero','round:1','foe',LifeState(20,5),0,own_spell_damage=True,hostile_not_farmed=True) is None and ('a','zero','round:1') not in w.drain_used)
    p=w.drain('one','a','zero','round:1','foe',LifeState(20,5),1,own_spell_damage=True,hostile_not_farmed=True)
    check('one damage commits even zero formula',p['fundedAmount']==0 and ('a','zero','round:1') in w.drain_used)
    w.select_drain('a','fake','round:1','foe',eligible_before_damage=True)
    rejects('Agony/natural damage not spell',lambda:w.drain('fake','a','fake','round:1','foe',LifeState(20,5),10,own_spell_damage=False,hostile_not_farmed=True))
    p=drain(w,event='deadheal',root='dead',life=LifeState(20,0,dead=True),damage=20)
    check('dead owner never resurrects from drain',p['state'].dead and p['fundedAmount']==0)

    # Independent conservation oracle, exercising funding AFTER reductions and
    # ordinary versus Critical missing HP. No need to mirror helper internals.
    for reserve in (0,1,2,7,16):
        for hp in range(21):
            for critical in (False,True):
                for damage in (0,1,2,9,40,101):
                    for factor in (Fraction(1),Fraction(1,2)):
                        w=world(feats={'lifeleech'});w.owners['a'].recovery=reserve
                        life=LifeState(20,hp,wounds=(None,None,None) if critical else ())
                        p=drain(w,life=life,damage=damage,systemic_factors=(factor,))
                        if damage==0:
                            assert p is None;matrix+=1;continue
                        funded=min(reserve,(damage//2*factor).__floor__())
                        ceiling=19 if critical else 20
                        assert p['reserveSpent']==funded
                        assert p['actualHpGained']==min(funded,max(0,ceiling-hp))
                        assert p['genuineExcess']==max(0,funded-(20-hp))
                        assert p['reserveRemaining']+p['reserveSpent']==reserve
                        matrix+=1

    w=world(owners=('a','b'))
    for i in range(3):check('soul accumulation '+str(i),death(w,'death'+str(i))==1)
    check('both feats use one capped pool',w.owners['a'].soul_charges==3)
    check('full capacity has no latent fourth',death(w,'full','body')==0)
    w.owners['a'].soul_charges=0
    check('same body later death this rest spent',death(w,'redeath','body')==0)
    rejects('old death cannot be rescanned',lambda:death(w,'full','body'))
    w.completed_rest('a',1)
    check('new rest permits future new death of body',death(w,'future','body')==1)
    check('second owner independent',death(w,'future','body',owner='b')==1)
    check('ineligible soul/object origin no charge',death(w,'object',qualifying_hostile_soul=False)==0)
    check('out of range death recorded ineligible',death(w,'far',legal_range_perception_line=False)==0)
    rejects('moving closer cannot rescan',lambda:death(w,'far'))
    w=world(feats={'soul_cage'})
    check('Soul Cage capture requires physical crystal',death(w,'no-crystal')==0)
    check('decline consumes eligible opportunity',death(w,'decline','body',crystal_available=True,accept=False)==0)
    check('declined body cannot retry this rest',death(w,'decline-redeath','body',crystal_available=True)==0)
    check('another body may capture',death(w,'other',crystal_available=True)==1)
    w.release_souls('a',1,actual_quiet_minute=True,crystal_available=True)
    check('quiet release dissipates owner charges',w.owners['a'].soul_charges==0)
    w=world(feats={'lifeleech'});death(w,'spark')
    rejects('Lifeleech alone cannot spend through unowned feat',lambda:w.begin_soul_ability('spend','a','a','shield',Wallet(),legal=True,crystal_available=True))

    w=world();w.owners['a'].soul_charges=3;strong(w,'a'); wallet=Wallet()
    w.begin_soul_ability('shield','a','a','shield',wallet,legal=True,crystal_available=True)
    offer=w.finish_soul_shield('shield',(8,8),0)
    check('self shield pays before failed arbitration',not offer['accepted'] and w.owners['a'].soul_charges==2 and not wallet.bonus_action)
    rejects('shield replay rejected',lambda:w.finish_soul_shield('shield',(8,8),0))
    rejects('lost crystal prevents ability',lambda:w.begin_soul_ability('lost','a','foe','agony',Wallet(),legal=True,crystal_available=False))
    check('lost crystal did not erase owner charges',w.owners['a'].soul_charges==2)
    p,result,wallet=lance(w,'lance',success=True)
    check('Agony pays Action/2 charges and half on save',result['damage']==6 and w.owners['a'].soul_charges==0 and wallet.actions==0 and p['dc']==15)
    check('Agony remains feat-owned damage',result['sourceKind']=='feat' and result['spellRoot'] is None and result['damageOwner']=='a')
    r=w.agony_reduction('foe',0)
    check('successful save still applies separate healing rider',r is not None and r.value==Fraction(1,2))
    lance(w,'lance2',now=30)
    check('same-family reapplication refreshes not multiplies',len(w.agony)==1 and w.agony['foe']['expires']==90 and len(w.agony['foe']['contributors'])==2)
    hp=healing_packet(LifeState(20,0),12,reductions=(w.agony_reduction('foe',30),))
    check('repeated lances still exactly half heal',hp['actualHpGained']==6)
    w.commit_healing('heal',hp)
    check('commit consumes single family record',w.agony_reduction('foe',31) is None)
    rejects('healing commitment replay rejected',lambda:w.commit_healing('heal',hp))
    lance(w,'lance3',now=100)
    hp=healing_packet(LifeState(20,20),4,hp_gain_prohibited=True,reductions=(w.agony_reduction('foe',100),))
    w.commit_healing('blockedheal',hp)
    check('positive potential consumes despite later prohibition/cap',not w.agony)
    lance(w,'lance4',now=200)
    hp=healing_packet(LifeState(20,5),0,reductions=(w.agony_reduction('foe',200),))
    w.commit_healing('zeroheal',hp)
    check('zero potential does not consume next-heal record',w.agony_reduction('foe',201) is not None)
    hp=healing_packet(LifeState(20,5),4,reductions=(w.agony_reduction('foe',201,suppressed=True),))
    w.commit_healing('suppressedheal',hp)
    check('suppression defers effect and consumption',hp['actualHpGained']==4 and w.agony_reduction('foe',202) is not None)
    check('Agony exact elapsed expiry while suppressed',w.agony_reduction('foe',260) is None)
    lance(w,'lance5',target='a',now=300)
    w.completed_rest('a',1)
    hp=drain(w,event='drain-with-agony',reductions=(w.agony_reduction('a',300),))
    check('Lifeleech integrates same canonical reducer commit',hp['fundedAmount']==3 and w.agony_reduction('a',300) is None)
    lance(w,'lance6',now=400)
    rejects('generic cure cannot remove Agony',lambda:w.remove_agony('foe',explicit_removal=False))
    w.remove_agony('foe',explicit_removal=True)
    check('explicit source removal works',w.agony_reduction('foe',401) is None)

    report={'status':'PASS — candidate reference; independent implementation review pending',
            'feats':8,'checks':len(checks),'fundingBoundaryCases':matrix,'failures':[],
            'helperSha256':hashlib.sha256((ROOT/'tools/buffer_feat_playtest_rules.py').read_bytes()).hexdigest(),
            'checksPassed':checks}
    (ROOT/'docs/mechanics/BUFFER_FEAT_PLAYTEST_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='checksPassed'},indent=2))


if __name__=='__main__':main()

```


## Exact file: DescentReviewChanges/ReviewBible/docs/mechanics/BUFFER_FEAT_PLAYTEST_VALIDATION.json

```text
{
  "status": "PASS \u2014 candidate reference; independent implementation review pending",
  "feats": 8,
  "checks": 131,
  "fundingBoundaryCases": 2520,
  "failures": [],
  "helperSha256": "7231e190dc4aa6d80a32b293f6d6b7753d3ec2ac0e0b6c280308b58b491cb9c1",
  "checksPassed": [
    "all eight acquired once",
    "no repeated feat",
    "prerequisite empowered_summoning",
    "prerequisite lifeleech",
    "prerequisite field_medic",
    "prerequisite necrotic_affinity",
    "prerequisite soul_cage",
    "prerequisite inspiring_leader",
    "prerequisite blood_ritual",
    "actual selection required",
    "acquisition does not grant reserve",
    "completed rest fills finite reserve",
    "same rest cannot repeat",
    "level change is not refill",
    "actual ingredients spent",
    "cooked food has no pre-rest potency",
    "unfinished rest cannot empower",
    "PB increase never manufactures fourth food",
    "current PB determines finalized shield",
    "cannot finalize batch twice",
    "rejected Chef shield still consumes food and entitlement",
    "same recipient second Chef serving",
    "serving identity replay",
    "recipient own rest resets family entitlement",
    "chef next rest ends unused potency",
    "chef rest does not erase already granted shield",
    "failed rest retains ordinary paid food",
    "aborted batch never finalizes",
    "PB decrease leaves ordinary remainder",
    "exact 24h potency endpoint",
    "one minute eating required",
    "discarded item stays unavailable",
    "speech not completed early",
    "speech start snapshot and rejected offer consumption",
    "departing listener alone loses benefit",
    "different speaker same recipient cap",
    "speaker cannot target self",
    "interrupted speech cannot complete",
    "owned feat survives later CHA loss",
    "completed speech replay",
    "blood use commits at start",
    "blood level snapshotted at start",
    "blood ally exact one-hour deadline",
    "blood advantage exists despite rejected self shield",
    "unrelated save preserves advantage",
    "qualifying actual roll consumes independent rider",
    "post-rest tie grant belongs to new epoch",
    "interrupted ritual still spends use",
    "two genuine bodies receive independent creation shields",
    "ended creature loses grant",
    "same lineage recreation grants nothing",
    "fixed damage does not use rider",
    "rolled damage uses current PB",
    "shared roll/reissue same round cannot duplicate",
    "other creature own roll entitlement",
    "next true round qualifies",
    "unpaid root cannot be invented",
    "device/rebuild ineligible",
    "kit pays one actual use and BA",
    "canonical stabilization no HP and clears failures",
    "separate background recovery preserves recorded trigger",
    "no duplicate stabilization grant",
    "already Stable cannot trigger",
    "new actual episode / other method qualifies",
    "empty real kit rejected before action",
    "input LifeState not mutated",
    "optional declined melee rider retains turn",
    "melee critical doubles feat die",
    "extra Action does not refresh",
    "off-turn hit can qualify",
    "genuine extra turn qualifies",
    "no seal for nonfatal/THP-only harm",
    "same owner death redundant",
    "rank5 blocked; higher and unknown not inferred",
    "24h exact expiry",
    "separate owner seal remains",
    "generic cure cannot erase seal",
    "legal return closes exact old death",
    "new later death separately sealable",
    "reviewed reaction pipeline preserved",
    "uncharged acquisition cannot heal or create excess",
    "same root round entitlement remains spent after rest",
    "actual drain funds finite HP",
    "no after-the-fact retarget",
    "full HP finite excess spends remaining budget",
    "zero remaining cannot farm extra conversions",
    "child healing cannot copy or trigger resource gain",
    "authorized external conversion gets finite excess",
    "excess cannot spend twice",
    "prohibition spends no reserve or excess",
    "Critical ceiling loss is not automatically excess",
    "zero actual damage does not commit entitlement",
    "one damage commits even zero formula",
    "Agony/natural damage not spell",
    "dead owner never resurrects from drain",
    "soul accumulation 0",
    "soul accumulation 1",
    "soul accumulation 2",
    "both feats use one capped pool",
    "full capacity has no latent fourth",
    "same body later death this rest spent",
    "old death cannot be rescanned",
    "new rest permits future new death of body",
    "second owner independent",
    "ineligible soul/object origin no charge",
    "out of range death recorded ineligible",
    "moving closer cannot rescan",
    "Soul Cage capture requires physical crystal",
    "decline consumes eligible opportunity",
    "declined body cannot retry this rest",
    "another body may capture",
    "quiet release dissipates owner charges",
    "Lifeleech alone cannot spend through unowned feat",
    "self shield pays before failed arbitration",
    "shield replay rejected",
    "lost crystal prevents ability",
    "lost crystal did not erase owner charges",
    "Agony pays Action/2 charges and half on save",
    "Agony remains feat-owned damage",
    "successful save still applies separate healing rider",
    "same-family reapplication refreshes not multiplies",
    "repeated lances still exactly half heal",
    "commit consumes single family record",
    "healing commitment replay rejected",
    "positive potential consumes despite later prohibition/cap",
    "zero potential does not consume next-heal record",
    "suppression defers effect and consumption",
    "Agony exact elapsed expiry while suppressed",
    "Lifeleech integrates same canonical reducer commit",
    "generic cure cannot remove Agony",
    "explicit source removal works"
  ]
}

```


## Exact file: DescentReviewChanges/ReviewBible/docs/mechanics/BUFFER_FEAT_SOURCE_VALIDATION.json

```text
{
  "status": "PASS",
  "fullFeatSourceObjects": 8,
  "preservedFeatRegistry": 335,
  "sourceFileSha256": "842d14e868aa93d51fc6f21e39bc9dd3a1b872cdffcf467ffaa99a4cc3f779b6",
  "scope": "Exact original objects including legacy text and cross-feat dependency; no operational approval"
}

```


## Actual existing dependency excerpt: tools/form_temphp_playtest_rules.py
```python
class BufferLedger:
    """Grant identities persist after ending; no hidden shield or replay refill.

    expire() must run at actual scheduler deadlines. Side effects are returned
    as instructions; this helper never decides eligible conditions or cleanses
    automatically. A projection into Core is checked and reconciled atomically.
    """
    def __init__(self):
        self.grants={}; self.active={}; self.rest_epochs={}; self.damage_events=set()
        self.absorptions={}
        self.form_instances=set()
        self.spell_anatomies={}

    def amount(self,target):
        ident=self.active.get(target)
        return self.grants[ident].remaining if ident else 0

    def current(self,target):
        ident=self.active.get(target)
        return self.grants.get(ident)

    def validate_offer(self,grant,now):
        require(isinstance(grant,BufferGrant) and grant.state=='pending','Supply a new uncommitted grant')
        require(grant.grant_id not in self.grants,'Grant identity already processed')
        marker=clock_marker(now)
        if grant.expiry is not None: require(marker<grant.expiry,'Grant deadline already passed')
        if grant.rest_epoch is not None:
            require(grant.rest_epoch==self.rest_epochs.get(grant.target,0),'Stale recipient rest epoch')
        current=self.current(grant.target)
        if current and current.expiry is not None:
            require(marker<current.expiry,'Resolve existing scheduled expiry before offering a new grant')

    def offer(self,grant,now=0):
        """Caller pays the legal source BEFORE this nonstack comparison.

        No current reviewed source overrides equal-retains-existing. Noble's
        paired Smite components are merged BEFORE calling this method once.
        """
        self.validate_offer(grant,now)
        g=deepcopy(grant)
        if not g.remaining:
            return {'accepted':False,'amount':0,'grantId':None}
        self.grants[g.grant_id]=g
        current=self.current(g.target)
        if current and current.remaining>=g.remaining:
            g.state='rejected'; return {'accepted':False,'amount':g.remaining,'grantId':None}
        if current: self.end(g.target,'replaced')
        g.state='active'; self.active[g.target]=g.grant_id
        return {'accepted':True,'amount':g.remaining,'grantId':g.grant_id}

    def end(self,target,reason,*,now=None):
        require(reason in ('replaced','depleted','natural-expiry','long-rest','dependency-ended','body-ended'),
                'Unknown buffer ending')
        g=self.current(target)
        if g is None:return []
        if reason=='natural-expiry':
            require(now is not None and g.expiry is not None and clock_marker(now)>=g.expiry,
                    'Natural expiry requires the actual fixed deadline')
        events=[]
        if reason=='natural-expiry' and g.remaining>0 and 'overflowing-cleanse' in g.riders:
            events.append({'sourceId':g.source_id,'grantId':g.grant_id,'target':target,
                           'chooseUpTo':1,'eligibleConditions':('Frightened','Poisoned','Staggered')})
        g.state=reason; g.remaining=0; g.riders.clear(); del self.active[target]
        return events

    def expire(self,now):
        marker=clock_marker(now); events=[]
        for target in list(self.active):
            g=self.current(target)
            if g.expiry is not None and marker>=g.expiry: events+=self.end(target,'natural-expiry',now=marker)
        return events

    def end_dependency(self,dependency):
        identity(dependency)
        for target in list(self.active):
            if dependency in self.current(target).dependencies:self.end(target,'dependency-ended')

    def completed_long_rest(self,target,epoch):
        integer(epoch,'new recipient LR epoch',1)
        require(epoch==self.rest_epochs.get(target,0)+1,'Process each actual completed LR exactly once')
        g=self.current(target)
        if g and g.rest_epoch is not None:self.end(target,'long-rest')
        self.rest_epochs[target]=epoch

    def consume_linked_reaction(self,target,grant_id,wallet,*,legal):
        g=self.current(target)
        require(legal and g is not None and g.grant_id==grant_id and 'bloodshield-reaction' in g.riders,
                'No current legal Bloodshield permission')
        wallet.validate(action='reaction'); wallet.pay(action='reaction')
        g.riders.remove('bloodshield-reaction')
        return {'sourceId':g.source_id,'grantId':g.grant_id,'reactionSpent':True}

    def core_damage(self,target,event_id,state,resolved_damage,*,now=0,**core_options):
        """Already defended packet, exactly one Core HP/Wound/death resolution.

        Returned life state is authoritative. Source-specific same-packet
        replacements remain the caller's existing Core/death adapter obligation;
        finalize Druid reversion only AFTER those settle the actual state.
        """
        identity(event_id); key=(target,event_id)
        require(key not in self.damage_events,'Damage event already resolved for this character')
        require(state.temp_hp==self.amount(target),'Core temporary-HP projection differs from grant ledger')
        current=self.current(target)
        require(current is None or current.expiry is None or clock_marker(now)<current.expiry,
                'Resolve scheduled shield expiry before damage')
        result,events=damage_event(state,resolved_damage,**core_options)
        self.damage_events.add(key)
        g=self.current(target)
        if g:
            g.remaining=result.temp_hp
            if not g.remaining:self.end(target,'depleted')
        return result,events

    def necrotic_affinity(self,target,event_id,post_defense_damage,wallet,expiry,*,legal):
        """Reaction at post-defense/after-resistance stage, BEFORE old buffer.

        Caller verifies spell/supernatural necrotic origin and actual access.
        Use returned remainingDamage in the canonical packet, then finish below.
        """
        identity(target); identity(event_id); require_deadline(expiry)
        integer(post_defense_damage,'post-defense necrotic damage',1)
        key=(target,event_id)
        require(legal and key not in self.absorptions and key not in self.damage_events,
                'Legal pending unique necrotic event required')
        wallet.validate(action='reaction'); wallet.pay(action='reaction')
        absorbed=post_defense_damage//2
        self.absorptions[key]={'amount':absorbed,'expiry':expiry,'finished':False}
        return {'prevented':absorbed,'remainingDamage':post_defense_damage-absorbed,
                'isHealing':False,'isTransfer':False}

    def finish_necrotic_affinity(self,target,event_id,grant_id,now,*,living_holder):
        key=(target,event_id); pending=self.absorptions.get(key)
        require(pending is not None and not pending['finished'] and key in self.damage_events,
                'Finish once after canonical damage has actually resolved')
        grant=None
        if pending['amount'] and living_holder:
            grant=BufferGrant(grant_id,'feat:necrotic_affinity',target,target,pending['amount'],expiry=pending['expiry'])
            self.validate_offer(grant,now)
        pending['finished']=True
        return self.offer(grant,now) if grant else None


```


## Actual existing dependency excerpt: tools/healing_playtest_rules.py
```python
def healing_packet(state, base, *, dice_count=0, pre_flat_bonuses=(),
                   conditional_flat_bonuses=(), conditional_dice_total=0,
                   conditional_dice_count=0, per_die_bonus=0, per_die_bonus_cap=None,
                   systemic_factors=(), reductions=(), hp_gain_prohibited=False,
                   reserve=None):
    """Pure two-pass arithmetic for ALREADY ELIGIBLE modifiers/reducers.

    Base includes the printed formula and legal pre-resolution rolled dice.
    Flat class bonuses use strongest across pre/conditional sets. Callers own
    source limits, dice rolls, costs, next-heal consumption, copy/trigger rights,
    legal converters and per-round budgets. Excess is quantity, not permission.
    """
    for name,value in [('base',base),('dice count',dice_count),('conditional dice',conditional_dice_total),
                       ('conditional dice count',conditional_dice_count),('per-die bonus',per_die_bonus)]:
        integer(value,name,0)
    for value in tuple(pre_flat_bonuses)+tuple(conditional_flat_bonuses):integer(value,'flat bonus',0)
    if per_die_bonus_cap is not None:integer(per_die_bonus_cap,'per-die bonus cap',0)
    if reserve is not None:integer(reserve,'remaining recovery reserve',0)
    system=Fraction(1)
    for factor in systemic_factors:
        if not isinstance(factor,Fraction) or not 0<=factor<=1:
            raise SpellRuleError('Systemic factors require exact reduction fractions')
        system*=factor
    if len({r.application_id for r in reductions})!=len(reductions):
        raise SpellRuleError('One application may enter healing once')
    live=[r for r in reductions if r.present and not r.suppressed]
    groups={}
    for r in live:
        if r.group in groups and groups[r.group].kind!=r.kind:
            raise SpellRuleError('A reduction group cannot mix unreviewed profiles')
        previous=groups.get(r.group)
        if previous is None or (r.value<previous.value if r.kind in ('factor','blight-totem') else r.value>previous.value):
            groups[r.group]=r
    ordinary=[r for r in groups.values() if r.kind!='blight-totem']
    totem=any(r.kind=='blight-totem' for r in groups.values())
    def calculate(use_conditional):
        count=dice_count+(conditional_dice_count if use_conditional else 0)
        flat=max(tuple(pre_flat_bonuses)+(tuple(conditional_flat_bonuses) if use_conditional else ()),default=0)
        die_bonus=count*per_die_bonus
        if per_die_bonus_cap is not None:die_bonus=min(die_bonus,per_die_bonus_cap)
        potential=base+flat+die_bonus+(conditional_dice_total if use_conditional else 0)
        per_die=max((r.value for r in ordinary if r.kind=='per-die'),default=0)
        factor=system
        for r in ordinary:
            if r.kind=='factor':factor*=r.value
        adjusted=max(0,potential-count*per_die)
        ordinary_amount=max(0,(adjusted*factor).__floor__()-sum(r.value for r in ordinary if r.kind=='flat'))
        plans=[('compatible-local',ordinary_amount)]
        if totem:plans.append(('blight-totem-alone',(potential*system*Fraction(1,2)).__floor__()))
        branch,reduced=min(plans,key=lambda item:item[1])
        legal=0 if hp_gain_prohibited else reduced
        healed,report=ordinary_healing(state,legal,reserve=reserve)
        return {'state':healed,'positivePotential':potential,'postReductionAmount':reduced,
                'legalAmount':legal,'ordinaryMissingHp':state.maximum_hp-state.hp,
                'genuineExcess':max(0,legal-(state.maximum_hp-state.hp)),
                'reductionBranch':branch,'diceCount':count,**report}
    preview=calculate(False)
    eligible=preview['actualHpGained']>0
    final=calculate(True) if eligible else preview
    return {**final,'conditionalAddonsQualify':eligible,
            'previewActualHpGained':preview['actualHpGained'],
            'nextHealingCandidates':[r.application_id for r in live if r.next_healing and preview['positivePotential']>0]}


```


## Actual existing dependency excerpt: tools/core_playtest_rules.py
```python
def stabilize(state, d4, now_seconds):
    integer(d4, 'Stable recovery d4', 1, 4)
    integer(now_seconds, 'elapsed seconds', 0)
    if state.dead or state.stable or state.hp != 0:
        raise SpellRuleError('Only a living dying creature can stabilize')
    state.stable = True
    state.death_successes = state.death_failures = 0
    state.stable_until_seconds = now_seconds + d4 * 3600


def healing_ceiling(state):
    return max(1, state.maximum_hp-1) if len(state.wounds)==3 else state.maximum_hp


def heal(state, amount):
    integer(amount, 'healing amount', 0)
    if state.dead:
        raise SpellRuleError('Ordinary healing cannot restore the dead')
    out = replace(state)
    gained = min(amount, max(0, healing_ceiling(out)-out.hp))
    out.hp += gained
    if gained > 0:
        out.stable = False
        out.stable_until_seconds = None
        out.death_successes = out.death_failures = 0
    return out


```
