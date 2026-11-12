# Selected wire95 policy state audit

The opt-in capability is limited to `TestOnlySharedWorldPolicy` with the connected recipe-4 batch selected. The constructor runs complete validation before the capability receives its origin. It compares the actual content fingerprint, scope, wire and revision on each verified transition. Default simulations and unsupported selections retain the original full-history path. The opt-in is unavailable for Release.

## Configuration and initialization

- The selected shared policy holds fixture definitions and feature selections for the accepted encounter, observation, character/condition, work, inventory, Haven and manufacturing rules. Its configuration entry points guard selection before `initializationStarted`. `Initial()` sets that flag to true and constructs a fresh snapshot. Its content build and portable checks also run in the selected profile validation; the common validation method remains on both execution paths.
- The body policy configures deferred condition targets and pressure movement delegates from the shared configuration before initialization. The selected callbacks receive the detached snapshot and use its positions, work and calendar. The condition fixture copies and orders its authored events into a read-only collection. Those events apply only through the existing command and shared clock.
- The command path uses snapshot-owned revision, clock, receipt order, life, condition, job and RNG records. The resolver and replay receipt helper operate on the passed snapshot. The inspected selected-policy command, condition and observation sources have no wall-clock or independent random source. There is no runtime target-selection call during historical replay.

## Transition ownership

The Core transaction uses the same authority preflight for both modes, including inventory grants before duplicate lookup. It creates the candidate and actual authenticated receipt before validation. The checkpoint belongs to the owning Core origin and selected policy. It keeps a private encoded byte array from canonical verification. The candidate and the independent replay share no mutable storage with that byte array. The replay starts from a separate decode and appends the verified submitted receipt. Whole canonical equality includes past receipts, all current fields and future continuation records represented by the format.

The full check still validates the profile, source bindings, portable state and other domain invariants before the history comparison. It is used for external restoration and for all strict calls. A mismatch leaves the old state and checkpoint in place. There is no automatic reseal or weaker mode. The new Core origin creates no persistence dependency, and the LabModel checkpoint is excluded from non-Laboratory builds.

The focused controls exercise independent session ownership at the same revision, external capture mutation, mismatching predecessor bytes, a structurally encodable mismatched candidate, valid-checksum forged state and receipt history, frozen feature configuration, invalid and revoked requests, duplicate/stale/conflicting submissions, and the existing 512-receipt cap. The connected comparison also uses separate policy instances and compares both public command results and the entire serialized state to vectors generated on the accepted reference assemblies. The timing run repeats the actual connected history through newly constructed sessions on the same configured policy and verifies the same accepted output.

The audit covers the selected wire95 paths. Other fixture families and any future configuration-dependent mutable state need their own equivalence evidence before using this capability.
