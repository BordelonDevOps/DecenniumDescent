# Actual GPT Action-budget and Druid cadence clarification

Captured from Calibration Review on 2026-10-09. This supplements GPT_TEMPORAL_PARENT_BOUNDARIES.md. It confirms source policies only, not a runtime parent adapter.

ChatGPT said:

Confirmed. My parent-conference wording does not override the approved kernel’s Action/Bonus Action/Reaction rewind semantics.

The correct distinction is:

Historical activation/payment events are conserved. A later cast really happened in the discarded timeline; its cast/event ID, RP expenditure, per-rest use, concentration replacement history, and other conserved costs remain historical.
Current Action economy is snapshot-restored. Action, Bonus Action, and Reaction availability return to the initiative-start snapshot state as already defined by the foundational kernel.
Outstanding Time Loop Reaction debts are then overlaid on that restored Reaction state.
Retiring a post-snapshot cast during rewind gives no refund for the Action/BA/Reaction originally used and imposes no second charge. It is simply removal/reconciliation of the discarded-timeline effect.
Historical evidence that an Action occurred is therefore not the same thing as keeping the Action budget spent in the new iteration.

That is also the only reading consistent with the normalized Time Loop text: it specifically restores encounter state and names finite resources that remain spent; it does not declare ordinary Action/Bonus Action budgets permanently consumed across the loop. 
Pasted text

So I would correct my earlier phrase:

“RP/uses/actions already spent remain conserved”

to the more precise:

RP, per-rest uses, and other conserved finite costs remain spent; the historical Action/Bonus Action/Reaction activation event remains recorded, while the current Action/Bonus Action/Reaction budgets restore from the snapshot and then receive the existing Time Loop Reaction-debt overlay. Retiring the later effect neither refunds nor charges an action.

That is the rule implementation should use.

Druid cadence

The additional evidence also supports the cadence ruling from the parent conference. I do not see a remaining source ambiguity requiring the Druid parent adapter to reject cadence changes.

The frozen shared rules separate the three relevant pieces:

Dissonance is accumulated casting strain and does not clear merely because an encounter ends. Actual Short/Long Rest, meditation, idle-turn decay, Grounding, or other explicit events modify it. 
Pasted text
Refrain tracks repeated named casting. It survives idle/weapon turns unless an exact class rule clears it. 
Pasted text
A real Druid Shapeshift entry is one such explicit class exception: it clears Refrain/remembered spell while leaving Dissonance accumulated. The attachment states that Time Loop anatomy restoration is not another Shapeshift entry. 
Pasted text

The quote helper corroborates that these values are real inputs to subsequent spell pricing: current Dissonance determines the strain state/surcharge, while the prior spell identity and Refrain determine the next repeat addition. It merely quotes those current values; it does not invent a temporal reset. 
Pasted text

Therefore the explicit temporal cadence bridge should be:

CONSERVE CURRENT CASTING CADENCE. Time Loop does not assign snapshot values to dissonance, refrain, or rememberedSpell. It preserves their actual current canonical values through temporal restoration. No discarded-timeline idle turn, Grounding, vent, Shapeshift entry, short rest, long rest, meditation, or other cadence-changing event is replayed. Future genuine iteration-qualified events modify that current cadence normally.

That has an important consequence: if a post-snapshot real paid Shapeshift cleared Refrain and Time Loop later restores an earlier anatomical form, the Refrain clear remains. The old form returning is not another entry and does not clear it a second time. Conversely, if discarded-timeline spellcasting increased Dissonance/Refrain, Time Loop does not erase that casting-economy consequence while retaining its RP payment.

This is appropriately labeled a NEW temporal cadence bridge grounded in the existing frozen cadence rules, not an assertion that all 17 classes' specialized cadence hooks are now integrated. The attachment itself makes that scope distinction. 
Pasted text

So the parent conference remains:

SOURCE-DISCUSSED / IMPLEMENTATION-READY, with the Action-budget wording corrected as above and the Druid cadence classification confirmed.

Full Time Loop, the remaining integrations, and the final joint whole-game flow/GitHub gate remain open.

## Codex source qualification

The reply lists Short/Long Rest among possible cadence-changing events. The unchanged frozen common rules explicitly name Retune, long rest, limited meditation, qualified idle turns and Grounding; they do not authorize a new automatic short-rest Dissonance reset. The authored parent guide preserves those exact permissions. No recovery rule was broadened.
