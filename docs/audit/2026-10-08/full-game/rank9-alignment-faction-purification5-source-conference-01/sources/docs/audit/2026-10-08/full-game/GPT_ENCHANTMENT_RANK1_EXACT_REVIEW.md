# GPT exact review — twelve rank-one Enchantment spells

Conversation: Calibration Review
Turn: c3d6ad40-d199-4f8b-9a3c-3d2e03fd12a3

I reviewed all four numbered attachments as one packet, in order, with the PART headers removed. The candidate is the manuscript identified as SHA256 `212687265c7f5de5653ad10d728512f0bf234f1c7c3e18a8a2668224d851687c`, with the shared fields/HARD_GUARD/LIMITATIONS_SUFFIX applied as specified. :chatgpt-content-reference{index="0"}

**Disposition: APPROVE all twelve exact cards for provisional manuscript promotion. No functional text repairs are required.** The Alignment Suggestion and Resonance Influence interpretations below are binding review clarifications of the submitted wording, not candidate-field changes.

1. **Mesmerize — approved.** Stunned and unaware remain separate components. The hard-control allowance governs the Stunned package; blocking Stunned does not manufacture immunity to the independently printed unaware rider. Conversely, a narrower inherited-component immunity only suppresses that component under the existing condition rules. Unaware adds no Unconscious/Prone/crit/drop-item package and does not become a second hard denial. The future-target-end clock is correct. :chatgpt-content-reference{index="1"}

2. **Pacify — approved.** The WIS save and voluntary attack/damaging-spell prohibition faithfully operationalize the source without turning it into generic “cannot harm.” Delayed damage intentionally created by a selected spell mode counts; a later miss/immunity does not retroactively make that spell nondamaging. Existing committed actions are untouched, and the restriction does not consume the whole-Action guard merely because the target has few attractive alternatives. :chatgpt-content-reference{index="2"}

3. **Sleep — approved.** The ordered fixed-24-current-HP procedure, minimum cost 1, temp-HP exclusion, no-save resolution, and “budget spent before hidden defense/guard” rule are all approved. A helper's physical rousing Action ending **all ordinary Sleep applications on that creature** is also approved: multiple overlapping casts do not require multiple separate wake-up Actions. This ends only this named Sleep cause, not unrelated Unconscious causes. Positive post-defense/pre-temp-HP damage wakes after the already-determined attack/hit/crit outcome. :chatgpt-content-reference{index="3"}

4. **Confusing Flash — approved.** Neutral `1d2`, neutral victim selection, one ordinary attack only, no Multiattack/spell/resource expenditure, and safe-route Flee are correct. The Attack branch reserves the hard-control allowance when the future command is established; a blocked Attack branch does not convert itself into Flee. Replacement/nonbanking behavior is correct. :chatgpt-content-reference{index="4"}

5. **Distract — approved.** It triggers against a pending Action after commitment/beginning hooks and before the first main outcome. On failed INT save, the whole-Action cancellation is the hard component; OA suppression is independent. If another nested event eliminates the parent Action before Distract resolves, Distract correctly cancels nothing and claims no hard-denial allowance, while its independently earned OA rider may still apply. The per-creature/per-pending-Action attempt is claimed at Distract commitment even if Distract is later Counterspelled. Ordinary Counterspell remains separate. :chatgpt-content-reference{index="5"}

6. **Voice of Peace — approved.** The participant set is correctly snapshotted at successful application. Later allies are not automatically enrolled. Provocation checks the target's actual recognition of its own ally at the provoking event, preventing hidden-allegiance detection. Harm breaks on commitment, even if the attack later misses. Hearing/language/range are initial gates rather than continued tethers. :chatgpt-content-reference{index="6"}

7. **Command — approved.** The bounded dictionary and general one-word procedure are coherent. Approach/Flee use movement; Drop uses actual release permission once; Halt/Grovel persist for that affected turn. Other words cannot create more than one coherent ordinary behavior using existing permissions. Invalid/impossible/prohibited commands do not mutate into another command. Whole-Action components use the hard guard; non-hard movement/interaction portions remain independently possible where the word actually permits them. A later valid failed-save Command replaces the pending command rather than adding another action budget. :chatgpt-content-reference{index="7"}

8. **Hideous Laughter — approved.** Immediate Prone and separately maintained Incapacitated are correctly distinguished. The Incapacitated component claims the hard allowance once; if blocked initially, it does not wait to spring into existence later. Prone remains independently applicable. The **current-turn end repeat save** is approved: this is a specifically authored repeat-save cadence, not the shared “next turn” endpoint convention. If applied during the target's current regular turn, that affected turn can therefore grant its end save. Ending never stands the creature or restores already-ended concentration. :chatgpt-content-reference{index="8"}

9. **Faction Charm — approved.** Strong affinity is not Core Charmed. The one-hour duration, faction-related Persuasion advantage, application-time affiliation snapshot, and recognized-faction-agent harm ending are correct. Independent `caster/target/faction` records are approved: the same creature can have simultaneous magical affinity toward different factions, potentially conflicting, but those feelings do not compel a choice and social advantage still does not stack. :chatgpt-content-reference{index="9"}

10. **Alignment Suggestion — approved, with the recast baseline explicitly resolved.** The submitted baseline rule is correct: **when a new Alignment Suggestion resolves, calculate from the target's actual alignment state with every existing Alignment Suggestion overlay ignored, while retaining every independent underlying/current alignment effect.** The previous same-spell overlay is therefore never a staircase for another one-step shift. :chatgpt-content-reference{index="10"}

The exact consequences are:

- If the underlying target is Chaotic Evil and an existing Alignment Suggestion makes it effectively Neutral Neutral, a new cast computes from **Chaotic Evil**, not Neutral Neutral, unless some independent effect has actually changed the underlying axes.
- If Corrupted or another legitimate source changes an underlying axis while an overlay is active, that underlying change **is** part of the next cast's baseline.
- Only axes whose newly calculated value differs from that baseline receive overlay values.
- A failed-save cast producing no changed axis creates no new overlay and does not replace an otherwise still-existing valid overlay.
- However, the normal concentration transition remains independent. If **the same caster** recasts while concentrating on their old Alignment Suggestion, that old concentration/application has already ended at the new cast's concentration transition. A no-change result does not resurrect it.
- If a successful changed-axis application replaces another caster's still-existing Alignment Suggestion, the replaced same-spell application ends; its old concentration no longer maintains an effect. There is still only one Alignment Suggestion overlay on the target.
- Ending the new overlay exposes the **then-current** underlying alignment, not the historical baseline captured when it was cast.

That fully approves the anti-ratcheting architecture without changing the submitted field text.

11. **Resonance Influence — approved, including final-price ordering and Mage Spell Sharing.** The submitted order is controlling: calculate the spell's ordinary legal RP price first, applying the actual spell/source base price, mandatory extras, Dissonance surcharge, and all eligible class/source reductions or waivers with their own scopes/minimums; **then** apply Resonance Influence's final `±1`, floor 0. :chatgpt-content-reference{index="11"}

For the attached class interactions:

- **Mage Spell Efficiency, Wizard Spell Efficiency, Core Sync, Matrix Linking, Sacred Echo Slot:** their “minimum 1” restricts that feature's own reduction step. It is **not a universal final-cost floor**. If that feature produces cost 1, an active Ease may subsequently make the actual cast cost 0; Burden may make it 2. :chatgpt-content-reference{index="12"} :chatgpt-content-reference{index="13"}
- **Resonance Apex:** its reduction/waiver resolves first, potentially producing 0; Ease remains 0 and is consumed, while Burden makes the resulting spell cost 1. :chatgpt-content-reference{index="14"}
- **Mandatory spell extras**, including the referenced Resonance Shield `+1`, are part of the ordinary spell price before Influence. Ease can offset 1 RP of the resulting total unless that particular source expressly states an absolute nonmodifiable cost; none of the submitted Resonance Influence text creates an exception.
- **Mage Spell Sharing:** the feature activation itself is not the ally's qualifying spell cast. The Mage pays `4 RP + the shared card's printed RP cost` when sharing. The ally's later use is nevertheless an **actual spell cast with an RP-price interface whose payment has been explicitly waived to 0**. Therefore:
  - Ease on the ally → final cost remains 0 and Ease is consumed.
  - **Burden on the ally → final cost becomes 1 RP. The ally must pay that 1 RP at the shared spell's cast commitment.**
  - That does not retroactively increase, refund, or otherwise change the Mage's earlier Spell Sharing payment.
  - If the ally cannot legally pay the added 1 RP, that attempted shared cast cannot commit; Burden remains pending because an illegal/unaffordable attempt does not consume it.
  - Spell Sharing's limited-use window continues under its own rule. :chatgpt-content-reference{index="15"}
- **Cleric techniques** are expressly not ordinary spells merely because they spend RP, so Resonance Influence does not apply to them. Likewise, a nonspell Shaman/Mage/etc. technique does not qualify merely for having an RP price. :chatgpt-content-reference{index="16"}
- A **charge-only item spell with no RP-price interface** remains excluded exactly as authored.
- A genuine spell whose RP payment has been expressly waived/reduced to 0 remains eligible; the source's waiver is processed before this independent final modifier.

Thus the candidate's distinction between **“spell with RP interface currently priced at 0”** and **“effect with no RP-price interface at all”** is approved.

12. **Enthrall — approved.** Up to three targets, hearing at application, independent WIS saves, concentration up to one minute, and disadvantage on **all actual Perception checks** are approved. There is no caster/tone exemption because the rank-1 source does not print one. No passive `-5`, automatic Hidden, awareness deletion, Charmed, Stunned or Action loss is introduced. :chatgpt-content-reference{index="17"}

The preserved **rank-2 / Core 349 / 3-RP Enthrall placement remains UNASSIGNED / NOT SELECTABLE**. It is not an upcast, merged mode, or extra class grant. Its “all creatures that can hear you / WIS negates” source remains intact pending the future identity/access decision. :chatgpt-content-reference{index="18"}

### Promotion disposition

**APPROVED — all twelve rank-one Enchantment identities may be promoted exactly from candidate `212687...687c`. No card-field repair is required.**

After promotion:

**222 reviewed identities / 626 unfinished identities**

All existing balance questions remain open, particularly Sleep, Mesmerize, Distract, Command, Hideous Laughter, the canonical-alignment overlay, and RP-price manipulation. This approval is limited to the provisional tabletop manuscript and does not certify runtime implementation, numerical balance, whole-game integration, or publication readiness.

