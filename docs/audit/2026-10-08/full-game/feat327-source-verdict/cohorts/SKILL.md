# Skill — final source-authoring directions

FEAT327-SOURCE-2026-10-11; internal review document. No exact-card promotion. Read with FS-01–16 and the final supplement register. Original data and legacy alternatives are retained in the JSON register.

## SF-01 — Acrobatic Mastery (`acrobatic_mastery`)

**Disposition:** AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/skill_feat_operating_proposal_internal.json` `/records/0`; file SHA-256 `7c06a45502c746a5c2648c644b56c66c31a177caf732f5f76f0365a73dd20137`.

**Original question:** Bind Failure versus Critical Failure under task degrees, opposed-check loss, selection of the rerolled d20 under advantage/disadvantage, natural shifts, information window and mandatory new result. Define Long Rest recovery and interaction with other rerolls without assuming a daily clock.

**Decision:** Keep complete-procedure reroll before committed consequences; fixed-DC degrees and opposed-total loss remain different. LR is beneficial owner rest, not a daily reset.

### Complete authoring text

After an actual Dexterity (Acrobatics) task resolves to Failure or Critical Failure, or loses an opposed check including an initiating tie, and before its consequences commit, you may spend this feat's one long-rest use to reroll that complete check. NEW: reroll the entire original one- or two-d20 procedure with the same advantage/disadvantage state and the same modifiers. Keep the new result even if worse, recomputing natural shifts for a fixed DC; the opponent's already rolled total does not change. The reroll is part of the original paid action, not another movement attempt or escape Action. If another feature can alter a die, declare an eligible sequence before resolving it; this feat cannot reroll its own reroll, and no earlier result can be restored merely because the new result is worse. A purely Strength (Athletics) check does not qualify.

### Worked boundaries

**SF-01-E01.** DC 15, original natural 3 plus 3 gives Failure. Spend the use; the replacement natural 1 plus 3 becomes Critical Failure and must stand. The falling consequence occurs once after the replacement.

**SF-01-E02.** With advantage, original faces 2/4 and +3 fail DC 15. Replace both faces, not only the lower face. If replacement 1/8 gives 11, keep Failure; no second use is available until a completed long rest.


## SF-02 — Battlefield Tactician (`battlefield_tactician`)

**Disposition:** AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/skill_feat_operating_proposal_internal.json` `/records/1`; file SHA-256 `7c06a45502c746a5c2648c644b56c66c31a177caf732f5f76f0365a73dd20137`.

**Original question:** Bind Soldier to the actual class or another sourced credential and define tactics rolls against the20 basic skills. Preserve+2 as a task bonus, not an automatic attack, class save-DC or engine-resource improvement. Identify actual tactics situations and stacking.

**Decision:** Adopt the explicit Soldier-class acquisition bridge and existing-skill concrete planning predicates; no attack/DC/command gain.

### Complete authoring text

NEW: Soldier means at least one actually acquired level in the Soldier Base class; a background title, uniform, rank or NPC occupation alone does not satisfy it. Add +2 when the Director calls for an ability check whose declared goal is evaluating a concrete battlefield plan, deployment, approach, withdrawal or fortification. Intelligence (Investigation) analyzes visible formations and routes; Intelligence (History) recalls an actually studied battle or doctrine; Intelligence (Engineering) evaluates a constructed defense. Use another ability/skill only when the actual task warrants it, with PB once. Do not roll merely to obtain the bonus. The result supplies the ordinary task's actionable information or plan, not extra allied attacks, higher class save DCs, free Overwatch, advance knowledge of hidden forces or compelled obedience. Timing and information access belong to that actual planning task.

### Worked boundaries

**SF-02-E01.** A Soldier 1 with INT 14 and Investigation proficiency analyzes an observed barricade: d20 + INT + PB + 2. Their later crossbow attack receives none of the tactics bonus.

**SF-02-E02.** A character with a soldier-themed background but zero Soldier class levels does not meet this proposed acquisition gate.


## SF-03 — Beast Whisperer (`beast_whisperer`)

**Disposition:** AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/skill_feat_operating_proposal_internal.json` `/records/2`; file SHA-256 `7c06a45502c746a5c2648c644b56c66c31a177caf732f5f76f0365a73dd20137`.

**Original question:** Resolve natural1→2 before task-degree shifts, both dice under advantage/disadvantage and repeated rerolls. A2 can still fail critically by margin: preserve the current effect separately from the broader inactive legacy promise. Bound simple emotional communication, actual beast senses and no language/command authority.

**Decision:** Keep effective 1-to-2 face replacement with raw history, including rerolls; current effect does not promise immunity to critical failure by margin.

### Complete authoring text

On an actual Animal Handling check, replace every d20 face of 1 with an effective face of 2 before selecting the advantage/disadvantage die, calculating the total and applying fixed-DC natural shifts. Keep the rolled face in history, but use 2 for this check's natural-result rule. Apply the same replacement to any lawfully rerolled die. It is a replacement, not another roll or a reroll trigger. A margin can still produce Critical Failure; the broader legacy promise is not adopted. Through observable posture and audible sound, communicate a simple emotional intent such as calm, warning, approach or leave. The beast must perceive the relevant signal. This grants neither language comprehension nor obedience, a trained mount, communication through total sensory obstruction, nor a changed attitude. A check is required only where the ordinary interaction calls for one.

### Worked boundaries

**SF-03-E01.** At DC 20 with modifier +2, a raw 1 becomes effective 2, total 4. The result remains Critical Failure by margin, without a further natural-1 downgrade.

**SF-03-E02.** Disadvantage faces 1/17 become 2/17; select 2. A deaf beast that sees a calming posture may perceive that signal, but it receives no spoken instructions it cannot understand.


## SF-04 — Climb Anywhere (`climb_anywhere`)

**Disposition:** AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/skill_feat_operating_proposal_internal.json` `/records/3`; file SHA-256 `7c06a45502c746a5c2648c644b56c66c31a177caf732f5f76f0365a73dd20137`.

**Original question:** Resolve Athletics4+ and the actual walking-to-climb Speed binding, handholds/hands/anatomy, encumbrance, armor, terrain and dynamic Speed changes. Define checks on sheer/inverted surfaces, failure/fall consequences and which angle-only disadvantage is removed without granting adhesive support.

**Decision:** Keep current walking-Speed derived climb with real holds/support and shared movement expenditure. Inherited penalties apply once, not twice.

### Complete authoring text

While your current body has usable grasping anatomy and the surface has actual adequate handholds, gain a climbing Speed equal to your current legal walking Speed. Apply body, load, armor and condition limits that actually govern that movement; do not derive a fresh unpenalized speed. Expenditure still comes from the shared movement budget. A steep angle alone does not impose disadvantage on a required climbing check. A sheer or inverted route still needs a check and an actually supportable method: usable cracks, holds, rigging, an anchor or another explicit ability. This feat provides no adhesion to a smooth unsupported ceiling. The Director states grip failure, a fall or loss of progress before the check under the route's actual conditions. Other causes of disadvantage, required hands, hazardous surfaces and zero-Speed conditions remain.

### Worked boundaries

**SF-04-E01.** Walking Speed reduced from 30 to 20 gives climbing Speed 20 on a held wall. Moving 10 feet on the ground leaves 10 feet of this movement budget for climbing.

**SF-04-E02.** A perfectly smooth inverted ceiling with no anchor is not traversable solely with this feat. A rope-supported inverted traverse can be attempted, with no angle-only disadvantage but any actual slickness penalty intact.


## SF-05 — Cold Reader (`cold_reader`)

**Disposition:** AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/skill_feat_operating_proposal_internal.json` `/records/4`; file SHA-256 `7c06a45502c746a5c2648c644b56c66c31a177caf732f5f76f0365a73dd20137`.

**Original question:** Resolve Insight5+, the full minute of actual observable speech, hearing/language/access requirements and the opposed Insight/Deception tie rule. Define one genuine surface motive/pressure/goal, retries, duration and no telepathy, hidden fact creation or compelled truth.

**Decision:** Keep continuous actual speaking observation, understood interpreted channel, opposed tie, one evidence-supported motive and changed-evidence retries under completed LAX/EX58.

### Complete authoring text

Observe one actual creature speaking for a continuous minute, with sufficient access to its audible speech and relevant visible or otherwise perceivable behavior. NEW: understand that speech directly or through an actually present interpreter whose interpretation spans the observation; a written transcript alone is insufficient. At the minute's end make Wisdom (Insight) opposed by that creature's Charisma (Deception), with ordinary actual proficiency. Higher total wins; a tie yields no new insight. On success the Director supplies one genuine current surface motive, emotional pressure or conversational goal reasonably supported by the observation. It is a fact about that exchange, not an ongoing mind-reading effect, a lie detector, an exact secret thought or proof of the speaker's factual claims. To try again on the same issue, obtain materially new behavior, stakes or evidence. Time still passes and an unwilling subject may stop speaking or leave.

### Worked boundaries

**SF-05-E01.** Insight 16 versus Deception 16 leaves the conversation unchanged; no motive is revealed. An additional identical minute does not earn an automatic fresh attempt.

**SF-05-E02.** Success can reveal that a merchant urgently wants the meeting ended. It does not reveal the unknown name of the person they intend to meet afterward.


## SF-06 — Cultural Expert (`cultural_expert`)

**Disposition:** AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/skill_feat_operating_proposal_internal.json` `/records/5`; file SHA-256 `7c06a45502c746a5c2648c644b56c66c31a177caf732f5f76f0365a73dd20137`.

**Original question:** Choose actual History, Religion or supported culture-specific Lore credential; resolve duplicate training and whether expertise applies only to the listed cultural subject matter. Define an unsupported Lore label without inventing automatic knowledge, new histories or cosmology.

**Decision:** Adopt per-acquisition training snapshot and bounded History specialization; no new generic Lore skill or invented culture.

### Complete authoring text

At acquisition choose History, Religion, or one specifically documented culture-specific Lore credential. If you are not proficient in the selected credential, gain its proficiency. If you already are, use twice PB for that credential's checks concerning cultures, customs and historical context; other checks in the selected skill retain normal PB. NEW: snapshot which branch applies on acquisition. Later gaining proficiency from another source does not retroactively convert the initial proficiency grant into Expertise. If a chosen culture has no separate recorded Lore credential, record a bounded History specialization for that named existing culture. It gives proficiency only for that subject, or twice PB there if History or that same subject is already proficient; it never creates general proficiency in a twenty-first skill. Double PB replaces rather than adds to normal PB and does not stack with other Expertise. Preserve actual access to knowledge and existing canon. No cosmological fact or cultural history is authored by choosing the feat.

### Worked boundaries

**SF-06-E01.** An already History-proficient holder uses twice PB for a check about a known people's treaty custom. The same feat supplies no proficiency multiplier to an Engineering check about the load-bearing capacity of a wall.

**SF-06-E02.** An untrained character chooses Religion and gains proficiency. A later duplicate Religion grant follows its own replacement rule; it does not silently upgrade this feat to Expertise.


## SF-07 — Disguise Expert (`disguise_expert`)

**Disposition:** AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/skill_feat_operating_proposal_internal.json` `/records/6`; file SHA-256 `7c06a45502c746a5c2648c644b56c66c31a177caf732f5f76f0365a73dd20137`.

**Original question:** Resolve Deception4+, actual10-minute materials/kit procedure, creator versus wearer, identity constraints and detection. Define the+2 bonus layer alongside current Tailoring/Leatherworking task families and actor-specific attire checks without publishing private garment formulas.

**Decision:** Keep ten-minute physical preparation and wearer-owned bonus with actual attire-family eligibility; no new size, voice or credentials.

### Complete authoring text

Spend ten actual minutes preparing a physically plausible assumed identity using sufficient actual clothing, cosmetics, props and appropriate tools for the chosen disguise. Record its identity, wearer, materials and limitations. The feat owner gains +2 to their Deception checks to maintain that identity while actually wearing the prepared disguise; creating a disguise for another person does not give that wearer this feat's bonus. NEW: an existing prepared disguise made by another competent person can qualify when the holder wears it as intended. A disguise does not alter body size, anatomy, voice, knowledge, language, credentials or magical signature unless another source actually does. Detection uses the actual encounter's check and observer; success in preparation is not permanent immunity to inspection. Ordinary materials grant no extra numerical modifier. A reviewed tailored garment's own disguise/task bonus keeps its separate documented family and wearer restrictions. A ruined or incompatible disguise ceases to qualify until legally repaired or prepared again.

### Worked boundaries

**SF-07-E01.** The feat owner prepares an ally's disguise in ten minutes; the ally gets the physical disguise but no borrowed +2. The owner wearing their own prepared disguise receives +2 on the actual identity-maintenance check.

**SF-07-E02.** A small disguise cannot make a Large creature fit a human-sized doorway or supply a password. A successful clothing deception does not resolve either obstacle.


## SF-08 — Dungeon Cartographer (`dungeon_cartographer`)

**Disposition:** AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/skill_feat_operating_proposal_internal.json` `/records/7`; file SHA-256 `7c06a45502c746a5c2648c644b56c66c31a177caf732f5f76f0365a73dd20137`.

**Original question:** Define normal travel pace, actual visibility/recording tools, ten-minute mapping requirement and what reliable means. Bind map access/copies, actual users, retrace-check scope, changing routes and reshape invalidation; no omniscient floor map or automatic navigation.

**Decision:** Keep ten observable accumulated mapping minutes and source-granted normal-pace concurrent mapping only; use completed EX58 pace and changed-segment history.

### Complete authoring text

Use actual recording tools and observable route evidence to map while moving at the adopted normal travel pace. This expressly permits that narrow concurrent mapping; it does not permit another incompatible Watch job. NEW: track ten accumulated active minutes on one identified continuous route or area, pausing when unable to observe or record. After those minutes, the resulting map grants advantage to you and allies actually using an accurate accessible copy on checks whose purpose is retracing its recorded route. It conveys no unseen passage, secret door, current occupant or guaranteed safety. The map remains useful until the route is reshaped or materially changed; mark changed segments unreliable while preserving still-valid observations. A map of one path cannot supply advantage to another. The feat does not grant normal-pace stealth, foraging, scouting or unlimited movement.

### Worked boundaries

**SF-08-E01.** Six observable mapping minutes, a five-minute obscured halt, and four more observable minutes complete the ten-minute route record; the halt counts on the world clock but not as mapping.

**SF-08-E02.** After one bridge collapses, the old map can still guide the intact approach. It cannot grant advantage to cross the missing bridge or prove an unobserved alternate route exists.


## SF-09 — Field Surgeon (`field_surgeon`)

**Disposition:** AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/skill_feat_operating_proposal_internal.json` `/records/8`; file SHA-256 `7c06a45502c746a5c2648c644b56c66c31a177caf732f5f76f0365a73dd20137`.

**Original question:** Bind genuine stabilization of a dying creature through Medicine or an actual kit, action/payment and successful event timing. Resolve once-per-Long-Rest per recipient versus practitioner, positive-healing gates, anti-loop ledgers and coexistence with reviewed Field Medic tempHP. Stable/already-conscious/dead subjects do not manufacture a new stabilization event.

**Decision:** Adopt direct 1-HP recovery after genuine stabilization and shared recipient LR-offer lock; keep broad recovery blockers, independent Field Medic and existing bodily consequences.

### Complete authoring text

When you actually cause a living dying creature to become Stable by a legal Medicine stabilization or a real healer's-kit use, offer that recipient 1 HP. Use the ordinary Action/DC 10 Wisdom (Medicine) route or the ordinary Action/one-kit-use route; an independently owned feature may explicitly change that action cost. NEW: treat the 1 HP as a direct state-recovery grant following the completed stabilization, not ordinary rolled healing. Broad cannot-regain-HP restrictions and the living-target gate apply; it receives no ordinary healing bonuses. Record one Field-Surgeon-family entitlement per recipient's own completed-long-rest epoch, shared across all practitioners. Commit it on the eligible offer even when HP gain is blocked. The actual stabilization remains recorded; if recovery is blocked the creature stays Stable at 0 with its normal existing recovery deadline. If positive HP is gained, clear the obsolete Stable deadline normally. A separately owned Field Medic temp-HP offer still uses the genuine stabilization event, even if the recipient is now at 1 HP. Already Stable or dead creatures create no new trigger.

### Worked boundaries

**SF-09-E01.** Medicine succeeds for a dying recipient: record stabilization, then recover 1 HP and end zero-HP unconsciousness if no independent cause remains. A later practitioner cannot supply a second Field Surgeon point before that recipient completes a long rest.

**SF-09-E02.** Decay blocks HP gain: the recipient remains Stable 0 and the feat entitlement is spent. Field Medic may still offer its separately legal temporary HP, which do not wake the recipient.


## SF-10 — Forensic Investigator (`forensic_investigator`)

**Disposition:** AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/skill_feat_operating_proposal_internal.json` `/records/9`; file SHA-256 `7c06a45502c746a5c2648c644b56c66c31a177caf732f5f76f0365a73dd20137`.

**Original question:** Resolve Investigation5+, ten-minute scene examination, appropriate senses/access, actual successful check and a finite additional physical clue. Define no-extra-clue cases, repeat examinations, lost/moved evidence and no fabricated suspect identity or Director duty to create impossible evidence.

**Decision:** Keep real ten-minute examination and finite additional clue; no clue is invented by a successful check or second owner.

### Complete authoring text

Spend at least ten active minutes examining an identified scene with actual senses, light, physical access and tools appropriate to the proposed search. Then resolve its Intelligence (Investigation) task and ordinary consequences. On Success or Critical Success, reveal one additional physical clue that could reasonably have been discovered in the searched evidence, beyond the ordinary success information. NEW: before resolving the check, the Director records a finite eligible extra clue or that no further physical evidence is available. If none exists, say so; do not invent evidence or refund the elapsed time. Interpretations are distinguished from observations. Repeating an unchanged search, sharing the result or adding a second feat owner cannot clone the same clue into a new fact. A new area, technique, access or evidence can justify a different examination. Destroyed or moved evidence must actually be available to the method used.

### Worked boundaries

**SF-10-E01.** Ordinary success finds a forced lock; the feat additionally reveals an actual distinctive metal shaving caught in the frame. It cannot name the unknown culprit without evidence.

**SF-10-E02.** A thoroughly washed empty chamber may yield no surviving additional clue. Success confirms that no further physical clue is available to this examination; it does not create footprints.


## SF-11 — Intuitive Reflex (`intuitive_reflex`)

**Disposition:** AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/skill_feat_operating_proposal_internal.json` `/records/10`; file SHA-256 `7c06a45502c746a5c2648c644b56c66c31a177caf732f5f76f0365a73dd20137`.

**Original question:** Bind+2 initiative as the actual Dexterity check bonus, stacking with Alert/Alertness and other bonus families, future rolls versus rewriting established order, rerolls, injuries and extra turns. Resolve whether its source category affects acquisition only.

**Decision:** Keep +2 per new initiative roll; replace future stacking reference by this conference common convention; no PB or initiative reordering.

### Complete authoring text

Add +2 once to each actual initiative roll you make, after selecting the legal d20 result and alongside the current Dexterity modifier and other eligible modifiers. Retain applicable injuries and penalties. NEW: distinct Alert/Alertness source identities may contribute only if actually owned and operationally approved; neither comparison grants acquisition, and any future shared-family decision can replace this provisional stacking proposal. Rerolling an initiative roll recalculates this bonus once; it does not add the bonus again to the old total. Acquiring the feat after initiative is established does not move the character's existing slot. Extra turns, Actions and virtual deadline markers are not new initiative rolls. The Skill category identifies source/acquisition organization and does not turn initiative into a trained skill or add PB.

### Worked boundaries

**SF-11-E01.** A roll of 12 with DEX +3, this feat +2 and Concussion -1 totals 16; no PB is added without another exact feature.

**SF-11-E02.** Gaining an extra turn makes no initiative roll and adds neither +2 to the established total nor a new duration endpoint.


## SF-12 — Librarian's Eye (`librarian_s_eye`)

**Disposition:** AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/skill_feat_operating_proposal_internal.json` `/records/11`; file SHA-256 `7c06a45502c746a5c2648c644b56c66c31a177caf732f5f76f0365a73dd20137`.

**Original question:** Define substance versus verbatim recall, actual prior reading/study, language/decoding, damaged or altered memory, and quote/locate/compare check domains. Bind+2 to actual tasks without remote text access, automatic factual truth or free research/formula acquisition.

**Decision:** Keep understood substance and +2 actual quote/locate/compare task, not inactive +5/verbatim omniscience.

### Complete authoring text

Accurately recall the substance of text you actually read and understood. NEW: record the material and relevant studied passage when its existence or scope is uncertain; the benefit preserves the text's content, not whether its claims are true. Verbatim quoting, locating a passage or comparing previously studied writings can still require an appropriate actual check; add +2 to that check. Recalling a straightforward understood summary needs no artificial roll solely to obtain a bonus. An unread cipher, unknown language, unseen page or remote revision is not previously studied content. Loss or alteration of memory by an explicit effect follows that effect. Knowing that a formula was discussed does not provide all missing formula instructions, research success, ownership rights or a prepared spell. The feat neither stores a perfect visual copy nor grants live remote access to the original.

### Worked boundaries

**SF-12-E01.** The holder remembers that a read ledger claimed a payment was made. They do not thereby know that the payment truly occurred.

**SF-12-E02.** A check to quote a specific sentence from a previously understood chapter gets +2. A sealed page never read gives no qualifying memory.


## SF-13 — Lock Savant (`lock_savant`)

**Disposition:** AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/skill_feat_operating_proposal_internal.json` `/records/12`; file SHA-256 `7c06a45502c746a5c2648c644b56c66c31a177caf732f5f76f0365a73dd20137`.

**Original question:** Resolve Thievery5+ against current tools/skills; define complex locks, required implements/access, actual+2 check and trap eligibility. Resolve fail-by5 versus natural1 task downgrade, repeated attempts, multiple/independent triggers and magical locks. It does not waive physically triggered traps merely by renaming the task.

**Decision:** Keep complex-lock +2 and numerical failure-by-five protection only for failure-triggered traps; ordinary lock Action/DC15 remains the governing baseline.

### Complete authoring text

Add +2 on a lawful check to open a lock whose actual construction the Director identifies as complex before the attempt. Possess the necessary access and implements; the feat does not provide them or a universal permission to pick a magical seal. NEW: the source's protection applies only to a trap whose trigger is this lock-opening attempt failing. If the final total is less than DC by 5 or more, that protection does not apply and the trap's real trigger resolves. A natural-1 task downgrade without a five-point numerical deficit does not by itself remove this protection. Independent touch, proximity, damage, time, wrong-key or tampering triggers still operate at their own actual moments even on a success. A legally repeated failed attempt receives the same margin rule but spends its real time and remains exposed to all independent events; it cannot undo a previously triggered trap. Thievery's acquisition bridge is specified in the shared proposal.

### Worked boundaries

**SF-13-E01.** DC 18, final total 14 fails by 4: a trap triggered solely by failed picking is suppressed. Total 13 fails by 5 and receives no feat protection.

**SF-13-E02.** A natural 1 plus 15 gives 16 versus DC 18 and downgrades the task to Critical Failure, but the numerical deficit is only 2. A separate touch trigger still fires if its touch occurred.


## SF-14 — Master Tracker (`master_tracker`)

**Disposition:** AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/skill_feat_operating_proposal_internal.json` `/records/13`; file SHA-256 `7c06a45502c746a5c2648c644b56c66c31a177caf732f5f76f0365a73dd20137`.

**Original question:** Preserve compatibilityAliases as an alias of this source identity, not another acquisition or bonus. Resolve Survival4+, normal travel pace, actual track availability and environment, approximate count/size/age on success, task degrees and no information from nonexistent tracks.

**Decision:** Keep +2 and normal-pace tracking with real evidence; compatibility alias is one identity, not another grant.

### Complete authoring text

Add +2 on Survival checks whose actual purpose is tracking. Follow existing, perceivable tracks at the adopted normal travel pace and, on an actual successful tracking check, identify the approximate count, size and age of the tracks to the precision the evidence supports. NEW: use Wisdom (Survival) for following and reading tracks unless an actual task expressly calls for another ability. Record a range or uncertainty rather than fabricate an exact census from poor evidence. The normal-pace permission changes only the tracking activity and does not remove travel hazards, actual visibility limits, route access, cargo constraints or stealth penalties. No tracks, obliterated tracks or an unrelated map cannot become usable tracks solely because the feat is owned. Preserve `skill_feats1_master_tracker` as an alias of `master_tracker`; it adds no second acquisition or +2.

### Worked boundaries

**SF-14-E01.** Success may reveal roughly three Medium walkers who passed within the last hour. Intermixed prints may justify a count range rather than an exact identity.

**SF-14-E02.** A save containing both the current ID and its compatibility alias represents one feat and one +2 contribution, never +4.


## SF-15 — Rogue’s Escape (`rogue_s_escape`)

**Disposition:** AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/skill_feat_operating_proposal_internal.json` `/records/14`; file SHA-256 `7c06a45502c746a5c2648c644b56c66c31a177caf732f5f76f0365a73dd20137`.

**Original question:** Define declaration and charge use for automatic success on an actual allowed grapple/restraint escape check or save. Bind action/time, source-specific escape availability, multiple restraints, no-save/no-check prisons and physical destination. It does not automatically grant teleportation or an escape roll absent from the source.

**Decision:** Keep pre-roll ordinary success on one already-authorized escape; pay original Action and LR allowance, no new escape, teleport or critical benefit.

### Complete authoring text

Once per completed long rest, while actually Grappled or Restrained, you may declare automatic success in place of one check or save that the holding effect actually permits to escape. NEW: declare and spend the use immediately before rolling, after choosing the legal escape action and paying its normal action or other cost. This supplies ordinary Success, not Critical Success or a natural 20. For an opposed escape, it wins that one permitted escape contest. Resolve the printed successful escape outcome for the selected holding effect; independent grapples/restraints remain unless that source's single check ends them together. No-check prisons, an inaccessible release mechanism, unconscious action restrictions or a feature forbidding an escape attempt are not bypassed. The feat changes no location by itself and grants neither movement nor teleportation. The spent use is not refunded because another restraint still holds you.

### Worked boundaries

**SF-15-E01.** Spend an Action and the feat use on the one grapple's allowed Athletics/Acrobatics escape; it succeeds, but a separate magical restraint requiring its own save remains.

**SF-15-E02.** A sealed stone cell with no Grappled/Restrained escape check provides no eligible activation and spends no feat use.


## SF-16 — Runic Scholar (`runic_scholar`)

**Disposition:** AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/skill_feat_operating_proposal_internal.json` `/records/15`; file SHA-256 `7c06a45502c746a5c2648c644b56c66c31a177caf732f5f76f0365a73dd20137`.

**Original question:** Resolve Arcana5+, one-minute real study/sight/language requirements, school and activation-method information, harmfulness and mythic concealment. Define the no-trigger protection's exact scope against proximity/touch/time triggers without making all runes inert or granting activation/control/formula knowledge.

**Decision:** Adopt one-minute noncontact examination protection only against study-caused triggers; independent triggers/mythic concealment and surrounding text remain separate.

### Complete authoring text

Study one actual magical symbol for one continuous minute with sufficient direct perception of its relevant marks. NEW: passive visual or equivalent noncontact examination by this procedure is not itself treated as activating that symbol, including a trigger based solely on this feat's act of looking or recognizing. It does not suppress a trigger already satisfied by approach, touch, entering a ward, speech, a third party or elapsed time; those can interrupt or harm the scholar normally. Do not touch, speak an activation or cross a ward as a free part of study. At completion learn the actual school, activation method and whether activation is harmful. If the source has no school, report that instead of inventing one. An explicit mythic concealment blocks this information and is not dispelled. This is recognition of magical operation, not translation of arbitrary surrounding writing; ordinary language rules still govern quoted words and other text. Identification grants no control, disarming, copied spell or hidden formula.

### Worked boundaries

**SF-16-E01.** Studying a gaze-activated rune by this exact procedure does not activate it solely through that studying gaze. Crossing its separately specified threshold before the minute ends still triggers it.

**SF-16-E02.** A time-triggered mark activates at its deadline during the minute; the feat does not pause the deadline or retroactively finish the study.


## SF-17 — Silent Movement (`silent_movement`)

**Disposition:** AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/skill_feat_operating_proposal_internal.json` `/records/16`; file SHA-256 `7c06a45502c746a5c2648c644b56c66c31a177caf732f5f76f0365a73dd20137`.

**Original question:** Identify source authority for any difficult-terrain Stealth disadvantage; remove only the actual nonmagical terrain cause. Define half-Speed silent travel, costs on debris, sound versus visual detection, armor noise, legal Hide and magical terrain. No automatic Hidden or ignored movement cost.

**Decision:** Adopt predeclared half-Speed turn/traverse with ordinary terrain cost and only careful debris-footfall silence, not full sound/visual stealth.

### Complete authoring text

Remove only disadvantage on your Stealth check that an actual rule or stated terrain adjudication assigns because the terrain is nonmagical and difficult. Do not invent a default disadvantage for all difficult terrain. NEW: declare silent-debris movement before any voluntary movement on your turn; outside initiative declare it before the complete continuous traverse. Halve your otherwise current applicable movement Speed for that whole turn or traverse, including the Speed used by Dash, and pay ordinary terrain costs from that reduced budget. Changing movement mode or leaving the debris does not refund that interval's reduction. Your own careful footfalls and disturbed ordinary debris make no revealing sound from that traverse. This is a narrow sound suppression; carried clattering gear, speech, attacks, collisions, collapsing structures and other independent sounds remain. Actual difficult-terrain movement costs and body/load limits remain. Magical terrain's sound or disadvantage is not suppressed by the nonmagical clause. Observers may see, smell or otherwise locate you; use actual Hide/Stealth rules for those senses. The feat does not establish Hidden automatically.

### Worked boundaries

**SF-17-E01.** Walking Speed 30 becomes 15 for the declared silent turn. Ordinary difficult terrain costs 2 feet per foot, so that budget pays for 7.5 actual feet, or one whole 5-foot tile where whole-tile movement is used. A Dash adds the reduced 15-foot budget, not an unreduced 30.

**SF-17-E02.** A silent traverse across pebbles remains plainly visible in a lit corridor. A loudly rattling carried chain is a separate sound source.


## SF-18 — Silver Tongue (`silver_tongue`)

**Disposition:** AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/skill_feat_operating_proposal_internal.json` `/records/17`; file SHA-256 `7c06a45502c746a5c2648c644b56c66c31a177caf732f5f76f0365a73dd20137`.

**Original question:** Define formal diplomacy/negotiation/mediation and the actual Persuasion checks receiving+2. Resolve other skill/tool/attire bonus families, genuine social stakes and no automatic consent, compelled attitude change or universal discount.

**Decision:** Keep +2 purposeful formal Persuasion and actual understood channel; apply completed EX58 social agency, time and no automatic economic award.

### Complete authoring text

Add +2 to an actual Persuasion check conducted through diplomacy, negotiation or mediation of a stated agreement, dispute or exchange. NEW: formal describes an acknowledged purposeful exchange with an identifiable request and stakes, not a requirement for court clothing or an official office. The affected party must receive and understand the argument through a legal direct or interpreted channel. Use the social procedure's actual eligibility, DC, stakes, evidence, cost and retry rule. The feat supplies no automatic discount, consent, altered reputation, loyalty, treaty enforcement or permission to ask an impossible favor. A Deception lie, Intimidation threat or unrelated Performance does not receive this Persuasion bonus merely because it occurs in a negotiation. Clothing and other modifiers retain their actual separate qualifications and the shared proposed stacking rule.

### Worked boundaries

**SF-18-E01.** A clearly stated bargain for a real porter service can qualify for +2 on a required Persuasion check. The bonus does not remove the agreed wage or invent an available porter.

**SF-18-E02.** An Intimidation check threatening a guard gets no Silver Tongue bonus, even when described as hard negotiation.


## SF-19 — Spell Scribe (`spell_scribe`)

**Disposition:** AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/skill_feat_operating_proposal_internal.json` `/records/18`; file SHA-256 `7c06a45502c746a5c2648c644b56c66c31a177caf732f5f76f0365a73dd20137`.

**Original question:** Distinguish spellbook learning/copying, actual scroll duplication and Scribing craft formulas. Bind source access, repertoire/rank/language, half active time and25-percent mundane-material reduction with exact quantities/rounding; rare inks/unique components unchanged. Resolve Craftsman/Forge Dwarf/research reductions without creating a copying procedure or free outputs.

**Decision:** Keep authorized spell/scroll-copy scope and strongest separate time/material reductions, precise rounding, rare/unique exclusions; completed Scribing is not universal scroll duplication.

### Complete authoring text

First identify an actually authorized copying procedure and the exact spell or scroll, legal source access, rank, language/notation, ability/tool requirements, facility and recipient record. Reduce only that actor's eligible copying active time to one half and mundane-material quantities to three quarters; rare inks and unique components are unchanged. NEW: apply the strongest eligible reduction separately to each time/material category, rather than multiplying overlapping reductions. Wizard Spell Scribing therefore supplies the same half-time factor and its better half-cost factor for its own qualifying copying; owning both gives neither quarter time nor a second material discount. Convert to minutes and round the final active time upward to a whole minute. For divisible mundane inputs retain exact quantities; for indivisible items round required remaining units upward; a listed aggregate gp expense rounds upward to the next cp. Separately identify rare/unique inputs before applying a discount to a mixed bill. No classification from absence: an unitemized ambiguous special-ink bill must be resolved by its source procedure before a discount is claimed. Level-up free additions remain free. Matrix preparation, reconstructing unknown text from memory, formula research and copying an ordinary craft formula are not spell/scroll copying. A usable scroll can be duplicated only under a separately authorized scroll-production procedure; the feat supplies no procedure or item effect.

### Worked boundaries

**SF-19-E01.** A legal copying task costs 120 minutes, 40 gp mundane supplies and 10 gp separately identified rare ink: this feat gives 60 minutes, 30 gp mundane and the unchanged 10 gp rare ink.

**SF-19-E02.** A Wizard also owning Spell Scribing uses that feature's half time and half eligible cost, not 120×0.5×0.5. Four indivisible mundane sheets become three; one required sheet still remains one.


## SF-20 — Steady Hands (`steady_hands`)

**Disposition:** AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/skill_feat_operating_proposal_internal.json` `/records/19`; file SHA-256 `7c06a45502c746a5c2648c644b56c66c31a177caf732f5f76f0365a73dd20137`.

**Original question:** Define motion, poor footing and minor injury causes of Sleight of Hand disadvantage, especially existing Injury penalties versus disadvantage. Remove only qualifying causes; keep blindness, hostile interference, bad tools, no hands and other restrictions. Apply ordinary cancellation afterward.

**Decision:** Keep cause-specific disadvantage removal; existing numeric Injury penalties are not removed.

### Complete authoring text

For an actual Sleight of Hand check, remove each disadvantage cause specifically assigned to ordinary motion, poor footing or a minor injury. Then evaluate remaining advantage/disadvantage normally. NEW: a minor injury for this purpose must be explicitly recorded as imposing disadvantage on that check; the feat does not reclassify Wounds or erase an Injury's numerical penalty. It does not remove lack of hands, inability to act, blindness, hostile interference, inadequate tools, a separate condition's disadvantage or an impossible physical task. A deck's normal rocking can qualify as motion; a creature actively striking or grappling the hands is independent hostile interference. It removes a qualifying disadvantage cause, not the underlying danger, forced movement or chance of losing footing under a separate check.

### Worked boundaries

**SF-20-E01.** A rocking cart imposes motion disadvantage while darkness imposes another: removing the first leaves disadvantage. An actual advantage source then cancels the remaining disadvantage normally.

**SF-20-E02.** Fine-Motor Trauma's current -1 manipulation/tool penalty remains -1; this feat does not convert it into a removable disadvantage.


## SF-21 — Trap Sense (`trap_sense`)

**Disposition:** AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/skill_feat_operating_proposal_internal.json` `/records/20`; file SHA-256 `7c06a45502c746a5c2648c644b56c66c31a177caf732f5f76f0365a73dd20137`.

**Original question:** Resolve Perception4+, normal travel pace, passive detection procedure, actual senses and detectable clues. Define trap versus creature/spell/hazard, sight at the saving-throw event and the+2 save modifier. Detecting a trap neither disarms it nor cancels unseen portions or independent triggers.

**Decision:** Keep actual passive Perception at normal pace and +2 save only with current trap sight; no invented passive ±5, detection clue or trap profile.

### Complete authoring text

At the adopted normal travel pace, you may use passive Perception to notice a trap's actually detectable clue. NEW: compare 10 plus the relevant Wisdom (Perception) modifier, with applicable PB once, to the trap's stated detection DC; meeting it notices the clue. There is no natural d20 or generic passive ±5 from advantage/disadvantage. A source explicitly requiring an active search or a different sense still controls; concealment, line, range and sensory access remain. Detecting a clue does not reveal every component or disarm the device. Add +2 to a saving throw against a trap you can actually see at the save event, including a visible operative component sufficient to recognize the incoming trap effect. A remembered location behind total visual obstruction is not sight. An ordinary creature attack or unrelated hazard is not a trap solely because it surprises you. If a source explicitly classifies a magical installation as a trap, retain that classification and its save rules.

### Worked boundaries

**SF-21-E01.** Passive 15 notices an accessible trap clue at DC 15 during normal-pace travel. A completely invisible clue with no applicable sense is not noticed by the arithmetic alone.

**SF-21-E02.** The character saw a floor plate earlier but is now blinded: its current save receives no sight-dependent +2. Remembering it can still inform a voluntary route choice.


## SF-22 — Unshakeable (`unshakeable`)

**Disposition:** AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/skill_feat_operating_proposal_internal.json` `/records/21`; file SHA-256 `7c06a45502c746a5c2648c644b56c66c31a177caf732f5f76f0365a73dd20137`.

**Original question:** Bind intimidation/coercion/fear as actual saves or opposed checks and identify the defending skill/ability, preserving+2. Resolve ordinary fixed-DC tasks, social influence, Frightened condition/escape saves and immunity versus bonus; no universal mind-control immunity.

**Decision:** Keep literal saves/contests against coercion/intimidation/fear; no fixed-DC task bonus or new social saving throw.

### Complete authoring text

Add +2 when you make an actual saving throw or opposed check whose operative purpose is resisting intimidation, coercion or fear. Use the defending ability/skill actually assigned by the effect or declared contest: for example Wisdom (Insight) against a manipulative Deception attempt only when the declared stake is coercive influence, rather than general lie detection. NEW: ordinary social exchanges do not gain an invented saving throw solely because you own this feat. A fixed-DC task check is not a contested check and receives no bonus from this wording unless another exact source includes it. An actual saving throw to end Frightened can qualify; immunity, an effect without a save and an automatic condition expiration are not bonus-bearing rolls. Retain binary-save rules, contested ties and all non-roll prerequisites. This does not change a player character's beliefs or compel an NPC to obey a failed check.

### Worked boundaries

**SF-22-E01.** A permitted Wisdom save to end a fear effect gets +2. A condition that ends automatically after one minute receives no extra roll from this feat.

**SF-22-E02.** A contested Insight defense against a declared coercive deception can qualify; an Investigation check to authenticate an unrelated receipt does not.


## SF-23 — Wilderness Chef (`wilderness_chef`)

**Disposition:** AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/skill_feat_operating_proposal_internal.json` `/records/22`; file SHA-256 `7c06a45502c746a5c2648c644b56c66c31a177caf732f5f76f0365a73dd20137`.

**Original question:** Resolve Nature4+ and define what the source's two bonus effects are, to which real forage output they attach, activation/duration/frequency/recipients and consumable cost. Compare reviewed Chef/Cooking/Herbalism/finite harvest without inventing extra biomass or treating legacy+10% as a second benefit.

**Decision:** Adopt explicitly NEW two finite riders, thirty-minute preparation, real safe forage portions, six-hour protection and one-hour +1 foodborne-save entitlement; no extra food or same-portion recipe stacking.

### Complete authoring text

The current source names two bonus effects without defining either. NEW complete proposal for discussion: once per completed long rest, after you personally finish a legal successful forage task yielding actual edible material, designate at most your current PB ordinary portions from that finite yield. Spend 30 active minutes with an actual cooking kit, safe heat and water if the food needs them to prepare those portions. No extra food, ingredients or Supply are created; record the original forage batch and its real quantities. Each designated portion has exactly two proposed riders: (1) Trail-ready preparation pauses its ordinary unprotected spoilage clock for the next six elapsed hours while kept clean in an appropriate container, after which its prior age resumes; breach or contamination ends this protection and other preservation does not add the intervals. (2) The eater may add +1 to one actual Constitution save against ordinary foodborne illness or food poisoning within one elapsed hour after fully consuming the portion, declaring before that roll. This does not work against magical poison, weapon poison, existing illness or non-food hazards. Record one recipient entitlement per completed long rest across all Wilderness Chefs; consuming another portion neither refreshes nor stacks it. Pay the cook's use at preparation start, even if interrupted. A poisoned or unsafe ingredient is not made edible; no other cooked recipe, Chef-serving or Feast effect is added to the same physical portion. These two riders are deliberately proposed new text, not recovered source or an interpretation of the legacy +10%.

### Worked boundaries

**SF-23-E01.** A PB 3 cook legally forages only two portions: the batch can prepare two, not three. It consumes real food and 30 minutes, and pauses each portion's prior spoilage age for at most six hours.

**SF-23-E02.** A recipient consumes two different cooks' portions before resting: there is one +1 entitlement, one fixed one-hour deadline from the first qualifying portion, and no +2 or timer refresh. A poisoned ingredient remains poisoned.


## SF-24 — Anatomy Lore (`anatomy_lore`)

**Disposition:** AUTHOR_FROM_EXACT_REPLACEMENT_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/skill_feat_operating_proposal_internal.json` `/records/23`; file SHA-256 `7c06a45502c746a5c2648c644b56c66c31a177caf732f5f76f0365a73dd20137`.

**Original question:** Bind Knowledge (Monstrous Humanoids) OR Survival to actual credentials; Bonus Action, range/line, one weak-point mark and expiry. Define next-hit+50% damage OR Huge-target advantage choice, payment/miss handling, short-rest Strength save DC and half-Speed timing. Resolve Precision Strike/Giant Slayer/critical multipliers without anatomical or cosmological retcons.

**Decision:** Preserve source next-attack scope including spell attacks, remove invented weapon-only exclusion and percentage monopoly; retain real anatomy, one mark, Huge choice and the paid slow.

### Complete authoring text

As a Bonus Action, mark one actually visible Large-or-larger creature with a perceivable physical weak point and legal line of effect. NEW: maximum range 60 feet; keep at most one such mark, replacing the old one without refund. At marking choose damage mode, or advantage mode if the target is Huge or larger. The mark lasts until the end of your next original regular turn, using the current virtual-marker rules if initiative changes. It is consumed by your next actual attack roll against that target, hit or miss; attacks against others neither consume it nor receive its benefit. Damage mode applies to the next actual personally owned attack, including a melee or ranged spell attack. It adds floor(50% of that attack's nonnegative native damage after its actual critical-dice adjustment), once before saves/defenses. Include only the native attack's dice and ordinary native ability modifier. Exclude separate riders, Smite/sneak dice, copied/reflected damage and other percentage enhancements from the base. A spell with no attack roll cannot consume or benefit from the mark. Add this extra amount as the attack's native damage type before target defenses, once. Advantage mode gives advantage to that next attack; ordinary cancellation still applies. Once per completed short rest, after an actual hit from advantage mode against a Huge-or-larger marked target, you may spend the use to force a Strength save against DC 8 + PB + INT modifier. On failure halve that target's current applicable movement Speeds until the end of your next original regular turn; do not stack same-family halves. NEW: the rider can qualify when the feat's advantage was canceled, because the selected paid mode still applied. The creature must possess relevant anatomy; no taxonomy or immunity is rewritten. NEW distinct percentage feats each calculate their own eligible native base and add their separately floored amounts without compounding, under FS-04. Hostile movement reductions use the existing strongest-slow arbitration, not this additive damage rule.

### Worked boundaries

**SF-24-E01.** A marked native attack, including an eligible spell attack, totals10 after its native critical adjustment. Anatomy Lore adds5 before defenses; an independent eligible50% feat adds its own5, not50% of15. A separate1d6 rider is outside both native bases.

**SF-24-E02.** A Huge target is marked in advantage mode; disadvantage cancels advantage and the attack still hits. The short-rest slow use may be spent; its STR success prevents the slow. Its failed save halves Speed30 to15; an existing-10 hostile slow does not make that10.


## SF-25 — Beast Lore (`beast_lore`)

**Disposition:** AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/skill_feat_operating_proposal_internal.json` `/records/24`; file SHA-256 `7c06a45502c746a5c2648c644b56c66c31a177caf732f5f76f0365a73dd20137`.

**Original question:** Preserve all three clauses: actual Animal Handling/Survival advantage, successful knowledge check granting allies+2 to hit for1minute, and once-per-Short-Rest call within300ft/DC15 for one nonhostile CR≤1 beast and a simple task. Define action/time/targets/beneficiary range, existing eligible beast availability, travel, agency, communication, duration and command budgets; no summoned or duplicate creature.

**Decision:** Adopt bounded Action/DC/briefing/call completions with real beast, route and finite task; source allies includes eligible self and no second companion budget.

### Complete authoring text

Gain advantage on actual Animal Handling and Survival checks involving beasts; this alone gives no new permitted check or beast language. NEW combat-read procedure: spend an Action observing one visible actual beast within 60 feet with legal line of effect; make Wisdom (Survival) against DC 10 + its recorded CR, rounding the final DC upward. Do not infer a missing CR. On success learn its actual diet, temperament and observed combat habits to the extent those are knowable from the evidence. Choose participating allies within 30 feet who can perceive and understand your briefing; those allies gain +2 to attack rolls against that one creature for one elapsed minute. You may be included as an ally. Keep at most one active briefing per feat owner; a new successful briefing replaces the old. Same-feat briefings on the same attacker/target do not stack. The separate beast call takes one Action and spends the short-rest use at the attempt: call an actually present nonhostile beast within 300 feet, CR 1 or lower, through a signal it can perceive, and make Wisdom (Survival) DC 15. On success it approaches by its actual movement and a possible route, then attempts one physically safe simple task you describe: tracking, carrying within capacity, or a non-damaging distraction. NEW: its task lasts at most one minute from arrival, with an overall ten-minute deadline from the call; interruption, incapacity or an impossible route can prevent completion. The Director retains its actual agency and behavior; it does not obey suicidal orders or become permanently friendly. No eligible beast means no created beast, no roll and no spent use. This does not establish a summoned body, new stat block, extra offensive budget or player-owned combat companion. Any later command/control must follow an actual separately owned source.

### Worked boundaries

**SF-25-E01.** A CR 1 beast read uses DC 11. A successful understood briefing gives its selected participants +2 against that creature for one minute; a second owner's same-feat briefing does not make it +4.

**SF-25-E02.** A real nonhostile CR 1/4 beast 200 feet away may approach after a successful DC 15 call using its actual route. A sealed wall with no route prevents arrival; the successful call is not teleportation and its spent use is not refunded.

