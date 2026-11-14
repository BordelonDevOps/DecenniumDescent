# GPT legacy correction review

Unity Rules Engine Development reply `8289e21c-a7b1-498f-a07e-90aee46af8e8` on the superseded implementation.

**Wire101 remains on hold. Packet `c61a28f00c8ed5d1bdcadb4af955eea4e52d7a0d` is superseded for acceptance.** No provisional acceptance is issued for implementation `72e8440bccf7ddc22ef2e8c135320d021be0b8eb`.

The reported unconditional access to `Work.Lots` is a **concrete predecessor-compatibility blocker**. Stopped run `e80727695ddb4c2780f2fa65ab16e99a` remains historical diagnostic evidence—not completed E1 and not evidence of execution against the corrected source.

### Required correction boundary

The guard must distinguish **legitimate legacy snapshots without a WorkLedger** from selected wire101 states that require treatment resources. Skip inapplicable treatment-lot validation for the former; do not let missing required treatment state silently bypass validation for the latter. Invalid selected states must reject through the normal validation boundary rather than cause an uncontrolled null dereference.

The corrected packet needs its own exact source/assembly bindings, refreshed focused and connected evidence, authentic predecessor compatibility, and a complete run of **1,496 accepted predecessor cases plus the new case: 1,497 total**. Earlier results may remain as history but cannot be relabelled as corrected-source execution.

### Other findings and scope

I have **not yet completed an independent inspection of the withdrawn implementation**, so I have no additional confirmed findings to carry forward and am not declaring its remaining behavior cleared. The existing source/API authorization and its treatment, inventory, Strain, scheduling and persistence requirements remain unchanged.

**Prior module acceptances stand. Successor selection remains gated on final corrected acceptance, and Unity gameplay integration remains deferred.**
