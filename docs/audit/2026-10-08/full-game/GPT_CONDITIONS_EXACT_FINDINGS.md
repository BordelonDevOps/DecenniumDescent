I found **three concrete corrections** before I would close this bounded condition/recovery package. Everything else in the candidate is coherent enough to move forward, and the source text remains preserved. Pasted text

1. **Intoxication direct floors above 2 are still ambiguous — BLOCKER.** Your identified weak point is real. A temporary floor of 4 or 5 can outlive or expire independently of the level-4 recovery timer or level-5 death deadline, producing contradictory states. Restrict generic direct applications to floor 2.

   **Replace the condition application with:**
   > An effect that says **Intoxicated** without assigning a numeric Intoxication level creates a minimum effective score of **2** for its printed duration. It does not add dose-driven points. A source that explicitly sets Intoxication to level 3, 4 or 5 must separately state whether it adds dose-driven points or supplies its own duration/recovery procedure; until that source is individually reviewed, it does not create a generic higher timed floor.

   **Replace the recovery-guide model with:**
   > `effectiveScore = max(doseDrivenScore, activeGenericFloor2)`
   >
   > Generic direct applications never create floors 3–5. Levels 3–5 arise from the dose-driven track or from a separately reviewed source that explicitly integrates with that track.

   Then delete the clauses in the level-4/5 procedures concerning a direct floor remaining at 4 or clearing a direct floor of 5. This removes the impossible timer cases entirely. Pasted text Pasted text

2. **Tolerance timing currently overstates the source — CORRECTION.** The recovered rule says **“After three uses in seven days, effect duration halves unless dose doubles.”** The candidate says `"The third dose is the first tolerant dose."` Those are not the same. Pasted text

   **Replace with:**
   > Record doses in a rolling seven-day window. **After the third completed use within that window, Tolerance becomes active. Subsequent uses while Tolerance remains active have half duration unless the dose is doubled.** A doubled dose counts as two doses for tolerance, repeated-dose and overdose accounting, but it is one consumption event and causes at most one dependence save from that event. Seven full days with no dose clears Tolerance.

   If you intentionally want the third use itself shortened, that should be labeled a **NEW provisional interpretation** rather than source-preserved.

3. **Specific periodic timing needs an explicit exclusion from generic Bleeding/Burning ticks — LOOP RISK.** The shared rule says specific replacement timing controls its own record, but it does not quite say that record is excluded from the generic end-of-regular-turn selection. A card with its own tick cadence could therefore be read as resolving both. Pasted text

   **Add:**
   > A Bleeding or Burning record with an explicitly printed replacement tick timing is **excluded from the generic end-of-regular-turn record selection** and resolves only at its printed timing. It may still coexist with generic records unless its source says otherwise.

### Everything else passes this adversarial pass

I do **not** see another blocker in the following new decisions:

- inherited condition immunity suppresses only the covered component while parent clocks continue;
- Dazed's immediate mid-turn accounting and extra-turn handling;
- Exhaustion's derived maximum-HP calculation, source-linked blocked levels, Speed order, and resurrection-at-level-6 behavior;
- strongest-record Bleeding/Burning selection and legal magical healing ending Bleeding even when actual restored HP is 0;
- Core-specific Invisible location endpoint overriding the otherwise-conflicting generic unseen modifiers;
- recovered Prone movement and standing rules;
- Staggered destroying current Guard, blocking reacquisition while active, and allowing only one +5-foot rider per continuous episode;
- Corrupted's recorded individual alignment classification and no ancestry/faction inference;
- Withdrawal leaving deterministic Retune and Oracle RC untouched;
- Resonance Burn remaining preserved but inactive in the Dissonance configuration;
- public Unity 0–6 mechanics remaining separate from Director-only lore;
- project clocks using actual elapsed hours, nonrefundable costs, and no double-paying the same active time or Supply;
- the Corrupted, dependence and Unity projects have defined role, cost, DC, duration, success and failure endpoints;
- level-5 Intoxication's fixed deadline and three-Wound successful-care exception are bounded once the higher direct-floor mechanism is removed. Pasted text

**Disposition:** after those **3 corrections**, I would close the **28 Core condition identities + generic condition recovery procedures** as **REVIEWED and reference-VALIDATED within the stated DD16 scope**.

That closure does not include individual condition-producing spells/items, full stealth/vision, generic grappling/restraint combat procedures, substance balance, encounter hazards, or broader game readiness; those correctly remain separate rows in the 75-area ledger.