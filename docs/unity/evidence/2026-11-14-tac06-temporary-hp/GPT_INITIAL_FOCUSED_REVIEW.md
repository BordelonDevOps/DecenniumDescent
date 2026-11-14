# GPT focused review

Unity Rules Engine Development reply `0f49cf22-f646-4010-9a3d-505dc8ecd818`.

## TAC-06 wire102 Consume Decay — **focused hold: one verification gap plus E1**

**Reviewed implementation:** `ffac40df4b1339b408801261eeeab409a95c0d9f`
**Reviewed evidence:** `a192e0c3c977f7d47bbecd31c20ca5b5bdce908f`
**Controlling authorization:** `b61d8e3f-fcdd-4c90-8d15-7e3b98b4676a`

**The demonstrated single-source gameplay routes are supported. One concrete focused-evidence requirement remains unmet: the promised grant-identity/deadline arbitration controls. Final acceptance therefore is not held solely for the running regression.**

### B1 — strongest-only controls verify numbers, not grant identity and deadline

The approved contract explicitly calls for detached larger/equal/smaller offers **with distinct grant IDs and deadlines**. Those controls must establish which grant survives, not merely whether one point total exceeds another.

The registered case currently checks only:

`Replaces(2, 3)`, `!Replaces(3, 3)` and `!Replaces(4, 3)`.

`TemporaryHpRules.Replaces` accepts two numbers and returns `offer > remaining`. These assertions correctly verify the numerical comparison, but neither the function nor those assertions receives a grant identity or deadline. They therefore cannot establish equal-value identity retention, rejection of a losing offer’s longer duration, or replacement-endpoint isolation. The public walkthrough does not supply that missing contrast because each branch correctly has only one entitlement and one granting source.

**This is an unmet agreed verification requirement—not a demonstrated failure of either executed public route.**

**Smallest closure:** add the bounded detached, metadata-aware arbitration evidence using the shared grant-selection/application logic, with distinguishable existing and offered records:

| Contrast | Required result |
|---|---|
| Larger offer than **remaining** points | New grant identity and its own deadline win, even when the old grant originally offered more points. |
| Equal offer with a different/later deadline | Existing identity, remaining points and original deadline remain unchanged. |
| Smaller offer with a later deadline | Existing grant remains unchanged; the losing duration is not inherited. |

Also demonstrate that a discarded/replaced grant cannot later clear the winner at its old endpoint or reappear after the winner ends. Keep the legal source’s expenditure separate from selection of the surviving grant, as already authorized. Use the actual shared implementation, not a test-only reimplementation of the expected answer. These are the existing lifecycle requirements, not authorization for additional public powers.

**No second public source, additional entitlement, Long Rest route, live replacement scenario or live overflow hit is requested.** A narrowly scoped internal adjustment needed to expose and test that selection remains within the approved contract; another preliminary source/API proposal is unnecessary.

### Findings supported by the inspected evidence

**Activation and source boundaries — met for the selected route.** The resolver checks the selected hero and substrate, genuine later encounter, owning turn, pending choices, Action availability, capability, stationary approved position and clear five-foot access. It derives the offer from attained character levels, spends the Action and records the one use without an activation roll or time advance. The existing life record owns the numerical buffer.

**Early absorption and healing — met.** The registered case and public verifier check the actual three-point opportunity hit depleting the buffer while normal HP remains 26, the separate two-point hit reducing normal HP to 24, and the manufactured vial restoring two normal HP without refilling the buffer. The detached same-packet overflow control uses the shared damage resolver and verifies three absorbed plus two normal-HP damage. **That combination remains sufficient; no additional search for a live overflow packet is required.**

**Revised late route — acceptable.** Activation on a real hero regular turn after defender defeat but before the lawful encounter-close command fits the approved scope. Consume Decay has no requirement that an enemy remain alive, and the contract did not freeze the tentative turn-18 route. The inspected case checks genuine injury, lawful subsequent vial use, surviving temporary HP through closure and movement, and exact expiry. The retained final state is r204 at **`120653/2`**, with **26/26 normal HP, zero temporary HP**, and the expiry attributed to the original r193 grant.

**Persistence and compatibility — focused portions supported.** The record/codec binds activation and terminal history; the registered case exercises restored duplicates, revoked authority, conflicting IDs and atomic rejection of forged offer/end histories. The verifier compares the **17 early and 19 late checkpoints** across restored console, uninterrupted console and direct public replay. The retained compatibility report passes authentic wire96–101 controls, while the bindings preserve the wire95 Default/Fishing Trap reference identities.

The retained registered case, standalone **C# 9** compilation and all **18 static checks** pass. Those results do not independently close B1.

### E1 and final disposition

Run **`1f71da0cb8c1438cab264ea011f92ace`** remains pending in this packet. Its launch assembly hashes match the focused bindings, which identify source archive **`5ebc05a1178104b1956effe0c681ed34dd31846123dd3bd741c53ddc20cfddcd`**.

This finding does **not** invalidate the current run against its exact source. Retain its completed result. If closing B1 changes package or test assemblies, final execution evidence must bind the resulting assembly set; the current run cannot be relabelled as execution of changed bytes.

I inspected the implementation changes, activation/lifecycle record and codec, complete registered case, public verifier and retained results, compatibility/build reports, bindings and launch. **I did not execute tests, load binary saves or independently recompute hashes.**

**Written ruling: hold for B1 and completed exact E1. No other concrete blocker was identified in this review.** The two connected routes and detached overflow approach need no redesign. Prior acceptances stand; successor implementation and Unity gameplay integration remain gated.
