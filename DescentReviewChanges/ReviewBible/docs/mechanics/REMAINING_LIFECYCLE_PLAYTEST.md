# Remaining companion and structure lifecycles

**REVIEWED / reference-VALIDATED — selected80+5 lifecycle/object/command/guard interfaces.** The selected interfaces pass 129 targeted checks. This guide implements decisions from the source conference, boundary reconciliation, final profile discussion and first implementation review. It does not replace original cards or promote all 80 passages to complete abilities.

The [source register](REMAINING_LIFECYCLE_SOURCE_BINDINGS.md) preserves all 80 exact class passages, their hashes, individual roles and open work. Five frozen shared paragraphs support the targeting, command and hard-denial rules. [Source validation](REMAINING_LIFECYCLE_SOURCE_VALIDATION.json) and [transaction validation](REMAINING_LIFECYCLE_PLAYTEST_VALIDATION.json) are separate evidence. The earlier [creature](CREATURE_LIFECYCLE_PLAYTEST.md) and [device](DEVICE_LIFECYCLE_PLAYTEST.md) packages remain applicable only to their specified sources.

## Shared operation

One owner has one numbered-round companion Bonus Action command allowance and one offensive companion allowance across classes. The ordinary commands below require the owner's **original regular turn** and resolve once in its attached companion phase. This scheduling is **NEW integration** where a card says only once per round. Extra turns do not supply another ordinary issuance window or refresh commands, target extra Actions, regular markers, duration or recharge. Costs and current-round allowances commit on issuance; inability to execute later provides no refund. A future forced native Action instead reserves the resolution round's offense and releases that reservation if cancelled, retaining its already spent issuance Bonus Action.

Keep original source owner, current controller and creature identity separate. Current source-class attack statistics belong to the original source owner. Control does not substitute the controller's statistics or manufacture another body or independent turn. Use the same physical-body registry, owner command ledger, action/resource wallet, encounter hard-denial set and target extra-Action clock across all sources. A real rest/encounter/recharge transition supplies a canonical scope; choosing a different key in code never authorizes another use.

Created finite creatures and turrets use the HP-only layer: apply legal defenses and existing temporary HP, then ordinary HP; at 0 they end. They gain no player Wounds, Stable state, death saves, XP, loot, corpse, resurrection target or resource-farming rights. No repair, resurrection or autonomous damaging turn follows from the word companion. Soldier structures have their own states below. The existing body registry also records known created-object identities, so later relabeling cannot turn a wall into corpse fuel.

The reference helper is a bounded transaction model. The caller supplies source access, target and placement legality, player agency, active control, native capability, actual dice results, defenses, class-resource side effects, exact virtual deadlines and canonical recharge scopes. These assertions are mandatory inputs, not permissions created by the helper. Ordinary attacks, complete condition/rider execution, native-monster damage and the live scheduler are not implemented here. Use `RemainingWorld.damage/expire/end_choir` for these selected bodies; routing Choir through the generic finite-creature cleanup would omit its source-specific bursts.

## Cleric: Rite of the Crimson Choir

Spend an Action, 5 Conviction and 8 RP, once per long rest, to place four fanatics in legal unoccupied spaces within 30 feet. Concentrate for at most three rounds. Each has AC14, HP10, Speed30 and no Reactions. Conviction expenditure can vent Dissonance once under the established class rule; the helper does not invent a second vent.

The Finale explicitly permits one regular-turn Bonus Action/offensive command to authorize up to four surviving fanatics. Each can move up to its Speed and independently make one melee attack at reach5 using the current Cleric technique attack bonus, dealing 1d6+S necrotic on a hit. This is one shared command with up to four actual attack rolls.

A legal hit also heals the Cleric exactly 1 HP, at most 4 HP per numbered round, within maximum HP and all applicable healing restrictions. **The hit predicate is literal:** fully resisted or immune damage does not by itself cancel this 1 HP. A miss gives none. The earlier healing classification must not be read as `min(actualDamage,1)`. The caller applies ordinary healing eligibility, Critical limits and explicit healing-generation prohibitions; this is not resurrection or Wound removal. A hit result is settled once, and a cancelled attack cannot claim it.

**NEW event identity:** every fanatic has one explosion opportunity. It explodes when it reaches 0, when concentration actually ends, or at the third-round deadline. Each burst affects legal enemies within5, DEX save, 1d6 necrotic on failure/half on success. All four bursts can affect the same enemy when geometry permits; there is no invented shared per-target burst cap.

If an applicable `noDeathTriggers`, `noRetaliation` or `noDamageTriggers` restriction suppresses the zero-triggered burst, permanently settle that fanatic's opportunity and end it. It cannot wait for expiry to explode again. At a true source-wide ending, snapshot all surviving fanatics and their positions, prepare bursts in stable creation order, then remove them as that ending resolves. A prior zero-ended fanatic is absent. Mere suppression of output while concentration remains active is not concentration ending. No individual voluntary dismissal is granted.

Bursts are ordinary source-native Cleric-feature damage, not another command. They cannot trigger Choir's attack-hit healing, grant another fanatic explosion opportunity, or turn the fanatics themselves into corpse, XP, loot, Conviction or resurrection resources. They do not impose blanket damage/death/retaliation/resource/copy prohibitions on enemies. A meaningful hostile nonsummoned enemy damaged or killed by a burst can still qualify for Dark Conviction under that feature's actual encounter, timing and frequency gates. Unrelated target-side damage/death responses and established global copy/resource rules still apply normally. Already snapshotted source-wide bursts resolve independently. There is no repair or return of ended fanatics.

## Cleric: Ritual of Undeath

One Action, 3 Conviction, 6 RP and one long-rest use choose **Corpse Servant or Death Ward**. They are not both granted. Death Ward retains its already reviewed would-die replacement: one living ally within30, one minute, first actual would-die event leaves1 HP and the specified temporary creature typing; no Wound removal.

For Corpse Servant, choose a real available humanoid corpse within30 that died no more than60 seconds ago. **NEW body integration:** successful creation consumes the physical corpse into the servant; it is unavailable for other corpse targeting, anchors and resurrection. Ending the servant never recreates that body as available corpse fuel.

The thrall lasts three rounds, AC13, HP10, Speed30, finite HP-only. One shared regular-turn Bonus Action/offensive command permits one Cleric technique attack dealing S d6 necrotic. **NEW missing-profile completion confirmed by GPT:** melee, reach5 only. No ranged mode, multiattack or imported undead abilities. It disappears at0 or expiry without XP, loot, new corpse, Conviction or resurrection target.

## Oracle: Ledger's Command

Spend an Action and2 RC to target one or two eligible undead within4 tiles (20 feet); Bones mastery may raise that target maximum to3. Each must be nonlegendary with CR no greater than floor(Oracle level/2). Resolve initial and actual regular-end Wisdom saves; willing undead may waive each required save. A failed/waived initial save establishes control for at most two rounds. A successful initial save still spends the cast resources. Preserve native HP, AC, original stat provenance, body and initiative.

**Willing order:** a regular-turn Bonus Action commits the Oracle's shared command/offense and that target's canonical one-extra-full-Action allowance for the same numbered round. This allowance is shared with every other extra-Action source and cannot recurse. In the attached phase, recheck control, consent, capability and target legality. Resolve one consensual extra move/ordinary attack. The original creature retains its normal regular Action; a created standard companion still gains no autonomous damaging turn. Withdrawn willingness cancels without a forced substitute, hard denial or any refund.

**Hostile/unwilling order:** after the failed save, issue one future order replacing the target's next real regular Action. Spend issuance-round Bonus Action and reserve the offense in the actual resolution round. Do not grant an attached extra attack. Revalidate control, capability, legality and the canonical (encounter, Oracle, target) hard-denial allowance. Spend that hard denial only if the native Action is actually replaced. Cancellation releases unused future offense, retaining the spent Bonus Action. At most one pending order for a target exists in an application; all applications also share the canonical budgets.

After that Oracle-to-target hard-denial allowance is spent, later failed regular-end saves can only deny Reactions and set Speed0 until the next original regular end or earlier Ledger ending. No repeated forced attack, Dodge or movement is allowed. A successful save ends control and pending orders. Extra/replayed markers do not tick this process. Ended control cannot retain the soft effect. The caller must cancel/revalidate pending orders promptly when source/control/legality changes, including expiry.

Each ordinary commanded attack uses the native permitted attack bonus, damage type and reach/range, without multiattack, recharge/spell/resource powers or extra riders. **NEW deterministic damage cap:** compare its maximum possible noncritical ordinary damage (dice maxima plus flat modifier) to `8 × S + M`. Keep a profile at or below that maximum; otherwise substitute S d8+M for its damage formula only. Then use ordinary attack/critical rules. Do not roll a second competing cap packet or clamp actual rolled damage.

Controlled undead offer flat DR1 on their first qualifying positive incoming damage event each numbered round, at the ordinary flat-reduction stage. An active qualifying source consumes its opportunity even if an equal or stronger DR wins strongest-only arbitration. Two DR1 sources do not add to2. Losing/regaining control does not reset an already used opportunity. A source inactive at an earlier event may use its first eligible event after becoming active.

**NEW source-native interception:** once per entire application, after a successful single-target attack against the Oracle hits but before damage/on-hit consequences, choose an active controlled expendable undead. No Reaction cost is added. No ongoing distance tether is invented from the acquisition range. Resolve the common interception transaction below. Ledger has no per-creature attack-versus-interception round exclusion; do not import the Unbound restriction.

## Oracle: Ledger Unbound

The Action costs0 RC and uses its once-per-long-rest entitlement. Its enemy blast retains the already reviewed shared-roll, maximum-HP comparison and minimum1-HP floor: up to3 enemies within5 tiles, roll4 S d8+M once, cap each target at one-quarter maximum HP, CON half, never reduce below1. This lifecycle helper does not roll or replay that damage.

Raise up to3 selected real nonsummoned available corpse bodies in range as bone servants. Each distinct body is consumed and never reappears when its servant ends. Each servant has HP1, AC12+floor(PB/2), Speed30 and owner-PB saves; duration three rounds. These defensive creation statistics are the standard bounded chassis. Attacks use current original Oracle Revelation bonus for1d8+S necrotic. **NEW gap-fill:** melee reach5 only, no ranged mode or imported monster profile.

One shared regular-turn Bonus Action/offensive command allows only one servant to move/attack. At issuance, reserve that servant's numbered-round local mode as `ATTACK_RESERVED`; cancelled execution does not refund it. A servant without a reserved attack may instead be sacrificed using the Oracle's actual Reaction to intercept a qualifying incoming attack. Its local mode becomes `SACRIFICED`. The same servant cannot attack and sacrifice in one numbered round, but servantA can attack while servantB is sacrificed. Sacrifice has no additional offensive-companion debit. The original Oracle must still control its own servant. No XP, loot, harvestable corpse or RC is created.

**NEW buff membership:** snapshot up to3 undead already controlled before the new servants are created. Only those identities can benefit for the original three-round duration. While each is actually controlled, it adds currentS to the one shared commanded attack and offers first-damage DR1 as above. Lost control suspends; regained control restores the same identity during the original duration, without replacing recipients or resetting used reduction. New servants are excluded. The helper's attack-bonus query is a profile eligibility calculation: the caller certifies the one qualifying commanded attack and applies existing shared command/rider limits, never every hit or arbitrary attack.

### Common Oracle interception transaction

Use one real incoming attack ID and a canonical window shared by both variants. It must be an actual successful single-target attack **against this Oracle**, after the hit and before consequences. The first committed interception closes that attack's window. No second attack roll, damage transfer branch or replay occurs. The Oracle receives no damage or on-hit consequences from it. The interceptor receives the source's zero-HP assignment/sacrifice, which is not damage, Wound-producing damage, retaliation or resource generation. Then resolve its native legal0-HP lifecycle.

For existing native creatures, the helper returns the zero-assignment instruction to the caller; it does not rewrite arbitrary monster/PC state. The caller must certify control, source expendability, agency and native prevention rights, then apply that native lifecycle once. This cannot silently sacrifice a PC or bypass a legal death replacement. A preexisting ordinary body retains whatever same-body remains its native lifecycle allows. No new or duplicate corpse entitlement follows. Created Unbound servants simply end and supply no body fuel.

## Oracle: Haunted Boon V

Action,0 cost, once per long rest. This manifestation has no invented HP, AC, combat targetability, attack or companion command. It has ordinary sight/hearing and can follow only a personally traveled same-plane route within one mile, without crossing sealed planar barriers. Speaking requires willing dead spirits encountered. It cannot read minds or supply unknowable facts, remote real-time senses or the Oracle's senses.

**NEW task integration:** choose one mode: scout/observe, one assigned inquiry of willing dead spirits, or deliver one prophetic message. The one task includes outbound travel, its performance, attempted return and printed report. It ends after that return/report or ten minutes, whichever first. A delivered message remains delivered even if the scout expires during return. No remote report or telepathic final upload occurs if it expires before returning. The returned account/name must derive from actual observations/encounters. No numerical Speed exists in the supplied source; the Director/caller certifies a real timed route within the deadline. General travel timing remains later work.

## Paladin: Echo of the Fallen

Record an actual allied death inside this Paladin's aura during the current encounter. A finite summon merely disappearing does not qualify. No corpse is required, and “who died” does not impose a new requirement that the ally remain dead. Track use by **Paladin + ally identity + actual long-rest epoch**, preventing repeated deaths from making extra uses.

Spend an Action and10 RP and immediately resolve one mode, including on a genuine extra own turn if the Action and source budgets exist. The spirit is untargetable with no HP, AC, native turn, Bonus Action command, corpse or follow-on action. It is not resurrection.

**Strike:** require an actual recorded ordinary weapon attack bonus, base damage formula, type and normal range. Without a recorded weapon profile, Strike is unavailable. Attack bonus is the lesser of that recorded bonus and current PB+actual CHA. **NEW deterministic cap:** compare maximum noncritical ordinary base damage to8×S+M; use S d8+M if the recorded profile exceeds it, otherwise retain that profile. Preserve original damage type/range and apply ordinary critical rules after selecting the profile. No Smite, Sneak Attack, resource riders, procs, extra attacks or stat-block duplication. Commit the shared offensive companion allowance, but not its Bonus Action command.

**Guard:** choose a legal ally in the aura, granting+2 AC until the Paladin's next original regular start. No recorded weapon or offensive-companion debit is required. Both modes spend the same ally's long-rest use.

## Soldier: Palisade and materials

At Soldier5 the automatic Palisade engine grants construction; it is not a selected skill. Spend an Action, one actual carried kit and an encounter deployment to erect contiguous unoccupied10×5-foot ground within5, height5, AC12. It blocks movement and line of sight across its height; climbing uses10 feet movement, with actual geometry/cover adjudicated normally. Psychic/poison immunity applies.

**NEW construction snapshot:** maximumHP=max(1,5+actual CON at deployment). At creation with Soldier13+, double that value and grant area-damage resistance. Later statistics do not recalculate or heal existing construction. The intact-wall cap and encounter deployments are1 below13,2 at13+. A later cap decrease preserves existing walls but prevents further construction at or above the current cap.

States are intact, destroyed or dismantled. Only positive-HP intact walls count against the cap and grant the printed benefits. Deployment consumes one kit into the wall. **NEW material integration:** completed one-minute dismantling returns at most one reusable carried kit, with hard carried cap2. At2, no third kit, hidden cache, deferred credit or sale value is created. Dismantling does not refund the encounter deployment. Destruction releases intact capacity without a kit, use, salvage or reconstruction refund. A completed long rest with carpentry tools replenishes carried kits to2; it does not restore walls or reset encounter counters without an actual encounter transition.

Once per encounter, an Action plus actual spare parts restores currentM HP to an eligible positive-HP damaged wall, capped at creation maximum. No repair payment at full HP, no0-HP reconstruction, no kit/deployment reset. Material accounting uses actual inventory; reference supply units represent one real source-qualified kit, field-supply use or spare-part use, not a newly invented economy price.

Hold Position grants+1 AC/+1 saves while adjacent to your intact wall. Brace Line grants the specified ally2 flatDR only with the printed wall/ally/attacker geometry. Bonuses do not stack across Soldier walls; strongest flatDR applies. Full cover prevents targeting instead of adding another cover AC bonus. Palisade Synergy addsS once per own turn to an actual own ranged weapon hit while adjacent to your deployed intact wall; it does not apply to every shot, area save or turret hit.

## Soldier: turrets, Quick Deploy and named protections

**Turret Deployment:** Action, one short-rest use, choose **one or two** legal empty squares within10. This reconciles “up to2” targets with “deploy2.” A chosen single turret spends the full use; no later second placement. Validate a two-turret placement atomically. Each snapshots AC12+PB, HP2×Soldier level, immobile, duration three rounds. One shared regular-turn Bonus Action/offensive command fires one turret: range60, current original Soldier PB+actual DEX,1d6+currentM piercing. There is no autonomous fire.

There is no printed global2-turret cap. Another independently legal refreshed use can create another1–2 while the old set remains; all share one owner offense/command. Expiry/reclamation is administrative bookkeeping with no sale, salvage, inventory surplus, extra deployment or recharge reset.

**Quick Deploy:** Action, one encounter use and actual carried field supplies; one legal5-foot square within5; AC12/HP5, three rounds or destroyed, half cover and difficult terrain. One at a time. **NEW replacement:** a successful independent legal use administratively ends old cover immediately before placing the new. Invalid replacement leaves the old object untouched. No refund or salvage. It is not Palisade and receives no Palisade TierII, repair, Hold Position, Brace Line or Synergy.

Neither Soldier turrets nor these structures inherit Tinker Field Repair, Snap, protected Dissonance routing, Volatile Components, Recycling, Salvage or Tinker deployable slots by analogy. An exact future source must grant a cross-class right individually.

**Bubble of Discipline** is a non-HP protective zone with only its printed spell-attack AC, spell-save and once-total Reaction reduction. **Fortify Zone** is a non-HP firing-lane effect dependent on the conscious Soldier and printed range/attack geometry. **Wall of Aegis** is a creature flat-DR effect, not another physical wall. None grants an attackable/repairable/dismantlable anchor or Palisade Synergy. Real cover and an independently applicable DR effect can both operate, but flatDR still uses strongest-only arbitration. Complete zone targeting, duration and defense execution remain with the appropriate combat/defense interfaces.

## Classified guards and deferred work

All 80 source IDs are individually discussed. Anti-farm and agency passages constrain their own Conviction, BG, Momentum, RC, Blood Tithe, healing, kill and copy systems; they never create corpse or companion permissions. Prior healing, death, control, maximum-HP and damage-sharing component reviews remain component reviews. Incidental temporary-HP effects, the complete Time Loop snapshot, full forms, all unimplemented portions of these cards and full source-family integration remain open.

The bounded guide adds no named abilities. All NEW procedures above are explicit completions of already existing sources, with original text preserved. Global corpse decay/cleanup, natural creature rest/Hit Dice, complete scout travel procedures, balance, human playtesting and the full tabletop/video-game runtime are not closed by these checks.

[Final notebook disposition](../../../../docs/audit/2026-10-08/full-game/GPT_REMAINING_LIFECYCLE_FINAL_CLOSURE.md) confirms this bounded scope after the Choir provenance correction.
