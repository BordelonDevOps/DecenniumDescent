# One ruleset for tabletop and software

The owner specified in Calibration Review that the systems should be ready for a TTRPG or later video-game development. The [recorded exchange](../../../../docs/audit/2026-10-08/full-game/GPT_TABLETOP_ENGINE_CONTRACT_NOTE.md) establishes paired authoring: readable tabletop procedures and precise engine contracts for the same rules.

This is a design and validation standard, not a claim that the full game or a video game has been implemented.

## Required rule contract

Every operational option needs an exact source identity and a traceable disposition of any ambiguity. Internal helper aliases must map back to actual supplied cards, spells, feats or engine passages. They do not create new game content. Preserve original text and label new integration decisions separately.

The tabletop procedure and its reference model must agree on:

- activation, prerequisites, actions, resource costs and limited uses;
- legal targets, type, willingness, range, visibility and line of effect;
- timing, original regular-turn and numbered-round markers, upkeep and expiry;
- HP, temporary HP, maximum HP, conditions and other state changes;
- stacking, replacement, strongest-effect selection and cross-owner limits;
- event attribution, copies, transfers, independent components and trigger exclusions;
- creation, suppression, destruction, repair, replacement and reconstruction;
- zero amounts, maximum1HP, blocked gains, missing resources and simultaneous effects.

Choices and dice remain explicit inputs. A deterministic engine resolves the same declared choices and recorded rolls consistently; it does not replace a player's decision or fabricate a Director ruling. If a rule intentionally leaves a judgment to the Director, identify that decision and what the engine must request or receive.

## Evidence and presentation

Use worked examples and relevant invariant checks to show that the procedure conserves resources, respects limits, rejects replay and preserves event attribution. Keep validation claims bounded to the actual supplied sources and tested behaviors.

The player-facing rule must remain usable at a physical table without reading code, internal IDs or event-ledger details. Implementation references may expose those details in a separate view. Shared data and linked source identities should keep the views synchronized.

Closing one helper does not finish every caller dependency. Target legality, action availability, ownership and other delegated requirements must eventually have their own reviewed contracts; an unspecified caller is an open integration boundary, not a complete software engine.

Human usability, balance and publication remain separate evidence gates. A reference test passing cannot replace a table session, and prose approval alone cannot establish executable correctness.
