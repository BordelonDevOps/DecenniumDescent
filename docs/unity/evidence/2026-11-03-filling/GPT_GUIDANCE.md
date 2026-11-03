# Completion-time filling guidance

The direct owner answer “Adopt completion-time filling” is recorded in the frozen decision source beside this evidence. Guidance is explanatory and does not promote rules or supply additional owner approval.

Chat: [Unity Rules Engine Development](https://chatgpt.com/c/6ae59513-3008-83e9-a5c4-8b6c5c5b4206). Response `785548d5-81e3-58aa-8ca0-c54686a3d790`, 2026-11-03, after Codex reported the owner decision and implementation contract:

Recorded as **owner-approved prototype filling policy** within the linked proposal. Your bounded implementation scope is consistent with it.

One implementation invariant: releasing the source reservation must accompany the **actual source-stock decrement and traced destination increment in the same transaction**. Release alone does not move water. Preserve the transfer receipt so replay cannot duplicate either change; award no consumption or nutrition credit.

Paused material/capacity reservations and active-only opening exclusivity fit that scope. Keep ordinary vessel profiles distinct from the oil-flask profile, preserve older save meanings, and retain the stated tactical/event/topology gates. No additional gameplay decision is implied.

Implemented invariant: the detached transaction releases the filling claim, decrements actual source stock and creates a traced destination descendant before validation and commit. A committed command receipt prevents duplicate transfer. Tests distinguish transfer from progressive consumption.
