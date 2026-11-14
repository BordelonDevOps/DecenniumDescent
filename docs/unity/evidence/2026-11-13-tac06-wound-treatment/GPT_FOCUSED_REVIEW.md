# GPT focused review

Unity Rules Engine Development reply `24184d48-256e-47b8-bb94-20d085d298fb`.

## TAC-06 wire101 ordinary Wound treatment — **corrected focused review passes**

**Reviewed implementation:** `11a15fd6a69ba073a7443843eb913e132b97e270`
**Reviewed evidence:** `89ee841bf1a268a0eb0ce0375238b50392fabc1a`
**Controlling authorization:** `42be382f-900e-4497-817c-d778770ba6c3`

**Provisionally accept the corrected implementation and focused evidence. Final acceptance is held solely for E1: the completed exact-bound 1,497-case regression. No additional source correction, rebuild, restart or focused scenario is requested.**

### Findings

**Legacy WorkLedger defect — corrected.** The change makes the *unselected-profile* station-stock check null-safe. It does not waive wire101’s required ledger: core snapshot validation rejects a missing WorkLedger for the selected base schema before treatment validation runs. The original triggering case, `checksum_corruption_rejected`, now has a retained passing result. The withdrawn source and evidence remain superseded—not substitutes for corrected execution.

**Treatment authority, finite inputs and scheduling — met.** The implementation binds the exact station, adjacent companion, eligible healer, usable hand, clear access and actual Wound. Starting reserves the kit and both participants’ required occupancy, consumes one complete basket through WorkLedger, and neither advances time nor rolls. Patient occupancy is distinguished from healer labor, allowing the authorized Stable-zero patient without treating unconsciousness as worker capability. Completion rechecks access; interruption releases future occupancy and the kit without refunding consumed materials.

**The executed branches satisfy the approved outcomes:**

| Branch/event | Focused evidence |
|---|---|
| **Independent Stable recovery** | Treatment starts at `113673/2` with the companion Stable at zero. Native recovery restores **1 HP at `128033/2`**, with zero recovery-event RNG, while treatment remains active. |
| **Completed treatment** | At `171273/2`, **17 + 0 against DC 12** removes the sole Wound, preserving **1 HP and Prone**. Existing pressure still rejects the northward step; lawful paid eastward movement reaches `(2,2)` at r323. |
| **Interruption and restart** | Interruption after recovery produces no treatment roll, refund or Wound benefit. The second basket funds a fresh interval from `166400` to `195200`. Actual **natural 2** retains the Wound and adds **one shared expedition Strain to the companion**, not the healer. |

The registered control and public verifier explicitly check those events, the retained vessel identities and empty tare, and first-point Strain effects without premature attack/save penalties.

**Persistence, replay and compatibility — focused requirements met.** Treatment records bind receipts, exact times, stock claims, occupancy, check evidence and causal Strain. The controls distinguish structural rejection of missing Strain evidence from full-restore rejection of an encodable forged Medicine modifier, preserving the live state. Detached admission probes remain labelled. The refreshed packet records **30 success-branch plus 33 interruption/Critical-Failure checkpoints** compared across restored console, uninterrupted console and direct public C# replay. Authentic wire95 Default/Fishing Trap identities and wire96–100 continuation/cross-profile controls pass.

The corrected registered treatment case, standalone **C# 9** compilation and all **18 static checks** also pass in the retained reports.

### Sole remaining gate: completed E1

Run **`83f6cafe3ad64899baf206326e74c920`** must complete the exact **1,496 accepted predecessors plus `tac06_connected_wound_treatment_ordinary_supply_and_strain`**, with the established ordered assignments, loaded assembly SHA/MVID, journals and completion records.

The launch’s four assembly hashes match the corrected bindings. Those bindings identify source archive **`5b47cf24f279141f026df33ce9e24815d99cb50bbaee6bb7cbcfea3cdeb14c80`** and correctly leave the regression result pending.

I inspected the correction, treatment resolver and records/codec, shared-clock integration, registered control, public verifier/results, compatibility and build reports, and bindings/launch. **I did not execute tests, load binary saves or independently recompute artifact hashes.**

**Final focused ruling: hold only for completed corrected E1.** Prior acceptances stand. Successor selection remains gated until final acceptance; broader TAC-06/P1 completion, production authority and Unity gameplay integration retain their existing limits.
