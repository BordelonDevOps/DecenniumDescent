# Custom rider integration — working record

**In progress. DD16 remains open.** The generic 28-condition reference and recovery package are closed only within their stated scope. The [first custom-rider review](GPT_CUSTOM_RIDER_FIRST_REVIEW.md) establishes the approach below; the [second conference](CODEX_CUSTOM_RIDER_SECOND_CONFERENCE.md) supplies missing and additional active cards and asks for remaining decisions.

## Preservation and binding model

Retain original display names and exact effects. Assign source-qualified mechanical IDs. A family/eligibility tag permits a stated cure, immunity or cross-feature check; it never imports another member's penalties, duration, stacking or resource generation. Record source owner separately from class and application ID. A suppressed, expired or immune effect does not satisfy an active-effect hook. The registry must validate source card IDs and engine indices rather than merely count search hits.

Proposed record fields: `mechanicalId`, `displayName`, `familyTags`, `effect`, `applicationSource`, `ending`, `stacking`, `immunityTags`, `hookAliases`, `sourceExceptions`, exact source references and review evidence.

## First-review decisions

| Family/name | Preserved distinction or decision |
|---|---|
| Shaken | `warrior.shaken` is −1 attacks; `thief.shaken` is disadvantage on the next fear save, consumed by that save or expiry. Shiver's critical Reaction denial is a separate rider. |
| Weakened | Mage and Wizard Dreadblade each apply −1 attacks; Warrior applies −1 weapon/natural-weapon damage. Separate IDs can share `eligibility.weakened` for Judging Light. |
| Crippled | A new binding can identify an active Crippler poison package; consume the normal package with its next-attack penalty, but a critical half-Speed rider can keep it active. Crippling Strike required its own source check. |
| Bleed | Source-qualified records preserve magnitude, start/end tick, tick count, owner, stacking and cure exceptions. `family.bleeding` supports explicit immunity/cure hooks. Crimson Blood Echo's two-instance exception remains. No duplicate generic tick for a replacement-timing record. |
| Burn | Ongoing fire is distinct from Resonance Burn, inactive historical casting risk, and feature names such as Crown's Burn. A new next-turn fallback is end of next regular target turn only where the source/engine omitted start/end. |
| Oracle Dread | −1 attacks/saves. Shorter Reaction denial remains separate. Fear immunity applies only to an explicitly fear-based application. Dominion's Dread mode applies Core Frightened instead. |
| Grief | Grief and Grief Mark have distinct penalties and source IDs. |
| Doomed | Cleric healing reduction/buff acceleration is distinct from Oracle Mark of the Doomed. Marks confer only their printed rights. |
| Root/Slowed | Root sets Speed 0 without importing Restrained. Slowed-foe eligibility can cover explicit hostile Speed reductions/root, not every zero-Speed state or terrain/cargo/Exhaustion. |
| Cursed/Diseased | Classification metadata, without an invented global penalty. Do not classify protected Oracle Curse engines, oaths or ancestry as removable hostile curses. Individual cure/tier interfaces still need resolution. |
| Disoriented | New precise next-regular-turn bridge preserves Action and movement. Random first movement uses only legal movement, grants no free distance, and expires at that turn's end. |
| Stasis | Cellular Reconstruction is its printed source-local package, without Unconscious/Prone/death-save/adjacent-critical inheritance. |
| Silence | Generic Silenced does not end concentration. Explicit audible maintenance can fail under its own rule. |

## Additional evidence recovered after the first request

- `mage.base.fire.fire`: passive Focus Burn is 1d4 fire at start of next target turn; Inferno Lance adds 1d6 fire at start of next two turns. Repeated Burns refresh rather than stack. Elemental Surge references the passive profile. The second request asks how the two applications interact on one finisher.
- `thief.arch.crippling-strike`: CON save or half Speed until end next target turn; its original source calls this Slow. Proposed binding: slowed-foe, not Crippled solely because its name resembles Crippler.
- `warrior.supplement.wailing-eye-cluster`: actual duration is through end of target's next turn. The effect's penalties begin next turn; the second request distinguishes pending from operative for Terror Engine.
- `cleric.base.judgment.judgment`: Judged is −1 AC for two rounds; repeated applications refresh. Divine Invocation's Judgment mode uses the same state.
- `monk.hero.way-of-shadow.nerve-fade-technique`: Shadow Rot has maximum two rounds, stack cap two, start-turn psychic damage, distinct one/two-stack save penalties, end-turn WIS removal. Precise stack clocks remain under discussion.
- `oracle.supplement.bones.rotting-touch`: Decay is a bounded three-round package with no healing, −1 saves, limited allied added damage and nearby corpse-raising restriction; its damage rider is not doubled vulnerability.
- Vengeance Mark, Judgment Brand and Mark of Retribution have distinct riders but explicit shared Vengeance qualification. Crimson Blood Mark and Oracle Mark of the Doomed remain separate.
- Warrior Brutality Sense's Vulnerable is a quarter-HP/visibility eligibility flag for Warrior features, not generic damage vulnerability.
- Last Rites defines Turned as safe movement away without automatically adding Frightened or Action loss.
- Bloodbond is a defined damage-sharing link; Mirrorbind is an ability-capture procedure, not a global condition merely because it contains “bind.”

## Later dispositions and current work

The [second review](GPT_CUSTOM_RIDER_SECOND_REVIEW.md), [scope correction](GPT_CUSTOM_RIDER_SCOPE_REVIEW.md), [fire/cure review](GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW.md), [periodic profiles](GPT_PERIODIC_PROFILE_REVIEW.md), [refresh closure](GPT_PERIODIC_REFRESH_CLOSURE.md) and [generic/custom alignment](GPT_GENERIC_CUSTOM_ALIGNMENT.md) settle the former pending questions above. This working record's first-review section is chronological evidence; the later source-qualified registry and supersession control the current candidate.

The current registry has 57 definitions, 14 source-qualified hooks and 114 verified card/engine/spell/condition references. Its 84 interface checks cover ownership, shared periodic arbitration, quarter-HP snapshots, mark consumption, buff expiry, blocked HP recovery, cure triggers, duration refresh and extinguishing. It remains IN_PROGRESS and is not a live-app migration or balance certification.

“Your” uses character ownership unless the source restricts class/engine origin. Thief can use its owner's legal multiclass effects; Crimson technical engine triggers require Crimson instances. Ordinary Blood Curse Bleed remains explicitly removable despite its distinct healing-triggered save. Charmed now preserves Core's willingly-harm boundary, including foreseeable harmful areas and indirect effects without forced beliefs or allegiances.

Generic and custom Bleed/fire now share one periodic model; the earlier separate generic selection, DC tie-break, all-record Medicine cure and one-save-clears-all-fire clauses are explicitly superseded. The raw reviews and Core text remain preserved. See the [implemented exact review packet](CODEX_PERIODIC_EXACT_REVIEW.md).

## Historical open questions now resolved

Finish the second conference, exact application/eligibility records and meaningful regressions. Reconcile owner-versus-class restrictions explicitly: “your” and “by your Warrior features” are not identical phrases, so a class-origin restriction must be source-supported or labeled a new integration decision. Decide ordinary Bleed removal separately from magical healing; a special healing endpoint alone does not establish artifact-level immunity to a spell explicitly ending Bleed.

A source-faithful Charmed wording correction is also pending: Core prohibits willingly harming the charmer, which includes knowingly harmful area/indirect effects rather than only directly targeting it. Preserve player agency and do not retroactively treat unpredictable collateral as willing harm.

The broad application-phrase scan found names missed by the initial finite keyword list. Both scans are preserved as candidate evidence; neither proves exhaustive semantic coverage on its own. Apply the completed registry to all 17 class engines/1,223 active cards and all 72 currently operational ordinary spells, then extend it as additional spell/item/hazard records become operational.

## Bounded periodic closure

The [GPT disposition](GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW.md) confirms the periodic-family package as REVIEWED / reference-VALIDATED after the two material fixes. The overall registry remains IN_PROGRESS, with roots/slows/marks, curse/disease metadata, Strain namespacing and semantic completeness outstanding.
