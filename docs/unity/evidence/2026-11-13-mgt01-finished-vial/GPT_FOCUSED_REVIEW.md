Actual Unity Rules Engine Development reply `d1613151-2118-4ae9-825e-92cc1c7beb99`, recorded verbatim apart from trailing whitespace.

## MGT-01 finished-vial carrying — focused review passes

**Source:** `1adb50263f2dc3954ff55fbba77d46d916515d7c`
**Evidence:** `e8b44bd506a5df8d907f1a3b71b960144f25299a`
**Authorization:** `ffc9e6d7-4753-4166-9c51-a540557bb776`

**No concrete source or focused-evidence blocker found. Hold final acceptance solely for E1: the completed exact-bound 1,492-case regression. No correction, rebuild, restart or additional focused scenario is requested.**

| Acceptance group | Focused verdict |
|---|---|
| **Identity and handling** | **Met.** Actual settlement creates one linked dose/vial body. Paid pickup changes custody—not ownership—and occupies one hand. The existing carrying path counts its changing mass once. |
| **Remote use and consequences** | **Met.** The hero uses that same held vial beyond workshop reach, pays the Action and retains the empty vial. Sibling doses retain their bench restriction. |
| **Persistence and integrity** | **Met.** Explicit wire96/base90 selection, canonical restoration, duplicate/conflict handling and forged-state rejection preserve the approved boundary. |
| **Exact execution** | **Focused/build portions met; full regression pending.** |

The implementation preserves the one-body relationship through `ConnectedVialRules`, synchronized custody/location and the dose-derived mass. Remote use requires the selected vial actually held by the hero; it neither requires a second free hand nor falls back to workshop access. Existing condition and life-state drop paths invoke the same vial-drop helper.

The retained route reaches **(0,3)** and legally uses the dose at **26/26 HP**: actual faces **1 and 3**, **six potential healing**, **zero effective healing**, with the Action and dose spent. The same vial remains held, and burden falls by exactly **1/10 lb and 1/100 Load**. Restored console, uninterrupted console and direct public C# agree at all five checkpoints through **r164, clock `113429/2`**.

The mandatory-drop check is accurately labelled a **detached consequence probe from a genuine carried save**, not an executed or restored gameplay history. Together with the inspected production hooks, it supports this bounded requirement without inventing another encounter.

The focused case and standalone C# 9 compilation passed. The manifest correctly leaves the full regression incomplete. E1 requires **all 1,491 accepted predecessors plus the new finished-vial case**, with the established assembly, worker and ordered-journal bindings.

I inspected the implementation, validation/codec changes, focused control, walkthrough verifier/results, bindings and source-to-evidence comparison. **I did not execute tests, load binary saves or independently recompute hashes.**

**Final focused ruling: hold only for completed E1.** Prior acceptances stand; no successor is authorized here. Production authority and Unity integration remain deferred.
