Codex source follow-up, with corrections to our first conference. The coverage taxonomy has 75 rows, numbered 0–74; the ledger now reflects 75.

Approved V6 Player Rulebook DOCX evidence:
• Paragraph 8255: Instant Death applies when damage reduces you to 0 and the remaining damage equals or exceeds maximum HP.
• 8260: Death saves occur at the start of the turn, using d20 without modifiers unless a feature grants one.
• 8268: Reset both death counters when HP is regained or the creature becomes stable.
• 8270: Damage at 0 HP equal to or exceeding maximum HP causes instant death.
• 8274: A stable creature remains unconscious, makes no death saves, and regains 1 HP after 1d4 hours if not otherwise healed. Damage makes it unstable again.
• 8278: Most monsters die at 0; significant NPCs may use death saves at Director discretion.
• 8282: A melee hit reducing a creature to 0 may knock it out stable instead of killing it.
• 8286: Temporary HP is removed before normal HP; it does not restore consciousness at 0, cannot be healed and does not stack.
Core V2 paragraph 776 defines Unconscious as Incapacitated, unaware, dropping held items, falling Prone, and suffering critical adjacent hits. Prone is therefore already Core. Stable behavior, counter reset and ordinary healing are recovered V6 rules, not new inventions. Correct their provenance. Core V2 does not explicitly remove V6 instant death: retain it as a compatible underlying rule, resolved after damage totals and before a Wound save; dead targets do not make further Wound saves.

Wound audit: all eight approved Word books were searched for Injury table, critical or lingering injury, Critically Wounded and instant death. Both Core books reference an Injury table; no actual table was found. A full search of both Core books for wound, injury, maiming and Medicine found 41 public and 47 Director paragraphs, including specific restoration effects but no other ordinary treatment procedure. Current docs/data/src text searches found no table beyond these references and our audit. This is a gap in inspected current sources, not proof that every historical archive lacks it.

The Core book also has 28 named conditions, while its JSON has only 15. The additions are Addicted, Bleeding, Burning, Corrupted, Dazed, Exhausted, Intoxicated, Marked, Petrified, Resonance Burn, Unity Exposure, Withdrawal and Wounded. Their full operational integration will be the next conditions pass.

Please finalize the core resolution/HP/Wound proposal with this evidence. Resolve explicitly: does the half-maximum-HP Wound threshold use damage before or after temporary HP absorption? What does the maximum-HP-minus-1 healing ceiling do when maximum HP is 1? Use the original Wound count to determine death from a failed save at three Wounds. Stable recovery and rest recovery must count elapsed time once. Knockout must not bypass instant death or a fatal Wound save; confirm.

Given the current Injury-table gap, author a compact six-result provisional table with exact d6 results, penalties, stacking and ending. Link each injury to the Wound gained on failure by 5. Avoid random additional Wounds, permanent character deletion, turn loss or new healing loops. Label every new decision. Give an exact source/overlay precedence and event sequence that we can implement and test. I will adversarially review it before closure.