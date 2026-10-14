**Bounded closure is justified.** I do not see a remaining blocker in the corrected **28 Core conditions + generic recovery procedures**.

1. **Direct `Intoxicated` floor 2 fallback — ACCEPT, with one timing sentence.** A two-hour fallback is bounded and avoids indefinite generic Intoxicated. I would encode:  
   **NEW:** “If a direct `Intoxicated` application supplies no duration, its floor-2 application expires exactly two elapsed hours after application. Multiple direct floor-2 applications do not stack; the floor remains while any such application is active. Ending one floor never removes independent dose-driven Intoxication.”  
   This prevents ambiguous overlapping timers without touching levels 3–5.

2. **Direct jump from below 4 to level 5 — ACCEPT.** Level-5 emergency and Unconscious start immediately. Do **not** create a dormant level-4 timer or poison save. Successful level-5 care moves the creature to 4 and only then initializes the level-4 `1d4`-hour timer and poisoning save. That is considerably cleaner than parallel hidden clocks.

3. **Automatic failure — ACCEPT.** When a rule says a check/save automatically fails, there is no d20 result or final numeric total. Treat it as ordinary **Failure** unless that rule itself specifies another consequence. It does not automatically become Critical Failure and cannot satisfy “fails by 5/10” because no numeric margin exists.

4. **Ordinary grapple source distinction — ACCEPT.** Use the recovered V6 ordinary-grapple procedure for generic grappling, including its opposed Athletics/application/escape procedure, Action cost and permitted Acrobatics escape where sourced. Exact ties preserve the current state under the already-adopted opposed-check rule.  
   A class/spell/item that explicitly prints a fixed DC, save ability, different action cost, range or escape procedure uses that **specific card procedure instead**; it does not inherit the ordinary grapple contest on top of it.

### `Shaken` preservation

Your proposed strategy is correct and should be mandatory for DD16.

There is **no Core condition named Shaken among the 28**, and I do not have an explicit owner-approved/notebook-authoritative decision establishing one universal shared `Shaken` mechanic.

The available class material instead contains mechanically incompatible same-display-name riders:

- **Warrior / Carrion Signal Gland:** `Shaken` = **-1 attack rolls until end next turn**.
- **Thief:** `Shaken` = **disadvantage on the next fear save**, with Shiver Oil carrying that class-specific rider through its stated duration.

Those cannot safely be merged.

Use source-qualified mechanical identities such as:

- `warrior.shaken`
- `thief.shaken`

while retaining **Shaken** as the displayed/source name and preserving each original effect text/provenance.

The same rule should apply to any other non-Core duplicate label: identical words do **not** imply identical conditions unless a source or explicit owner decision actually unifies them. That is consistent with the existing project rule that Dread, Grief, Bleed and other custom riders use their own exact card definitions.

### Closure disposition

With the three previous corrections plus these endpoint clarifications:

**28 Core condition identities + generic recovery: CLOSED as `REVIEWED` and reference-`VALIDATED` within the bounded scope.**

The reported **82 checks + 4,200 Exhaustion-state scenarios PASS** supports that bounded validation state.

**DD16 remains OPEN**, correctly, because the next required pass is the inventory and reconciliation of **all operational custom/class/spell condition and rider names**, including collisions like `Shaken`.

This closure does not certify the wider combat engine, vision/stealth, every condition-producing card, substances/items, hazards, encounter balance, or the game as a whole.