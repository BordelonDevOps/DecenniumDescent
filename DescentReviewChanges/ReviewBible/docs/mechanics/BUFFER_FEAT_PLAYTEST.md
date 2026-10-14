# Eight feats: complete candidate rules

**REVIEWED / reference-VALIDATED for these eight full feats. Provisional playtest overlay; human numerical balance pending.** These rules cover Chef, Inspiring Leader, Empowered Summoning, Field Medic, Blood Ritual, Necrotic Affinity, Lifeleech and the Soul Cage **feat**. They do not authorize the separate Soul Cage spell or complete the other327 feat entries. Numerical balance still needs human playtests.

The335 original feat objects are preserved. [Actual GPT closure](../../../../docs/audit/2026-10-08/full-game/GPT_BUFFER_FEAT_FINAL_CLOSURE.md) reviewed131 targeted checks and2,520 funding boundary cases. The remaining327 feats require separate full-clause review. Source capture: `docs/audit/2026-10-08/full-game/BUFFER_FEAT_COMPLETION_SOURCES.json` from the game root. Decisions: `GPT_BUFFER_FEAT_FIRST_REVIEW.md`, `GPT_BUFFER_FEAT_BOUNDARIES.md`, `GPT_BUFFER_FEAT_FINAL_BRIDGES.md` in that directory. Later decisions supersede conflicting portions of the first draft. Reference adapter: `tools/buffer_feat_playtest_rules.py`; validation: `tools/validate_buffer_feat_playtests.py`.

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
