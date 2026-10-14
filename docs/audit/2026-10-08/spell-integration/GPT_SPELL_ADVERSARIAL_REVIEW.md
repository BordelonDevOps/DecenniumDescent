The 72-card packet is materially improved, but I would not freeze it yet. The ten conference issues mostly resolve cleanly; I found **12 remaining mechanical/source-interface corrections** worth applying before using this as the template for the next tranche. Pasted text

### Ten conference issues

1. **Core V2 metadata vs companion catalog — AGREE.** Retain both. Core V2 clearly supplies evidence absent from the companion view, but fields such as `"Automatic or opposed as described"` are frequently non-operational. New resolutions must remain explicitly provisional.

2. **Resonance Shield — QUALIFY.** Rejecting the fixed-5 version is correct, but the evidence is actually three-way: rank-0 source/Core says **1d4**, the companion rank-2 summary says **5 per RP**, and Core rank-2 says **2 per RP**. Using `class rank cost + mandatory 1 RP → 1d4 temp HP` is a valid provisional decision, not a fully reconciled source fact. Preserve all three variants in provenance.

3. **Restore coherent Core actions/ranges/components — QUALIFY.** Correct principle, and Alarm Ward/Mist Step are now aligned. However Shield, Predict Movement, Resonance Shield, and arguably False Life still override coherent Core 30-foot ranges. Those need explicit decisions below.

4. **Burning Hands / Hellish Rebuke DEX save for half — QUALIFIED AGREE.** Core's generic wording does **not** justify automatic damage. DEX-half is a reasonable bounded provisional resolution while keeping 3d6/2d10 unchanged. It must remain labeled new playtest mechanics, not recovered canon.

5. **Retune bridge — QUALIFIED AGREE.** The class formula plus two beneficial short rests/long rest and one beneficial long rest/24h prevents obvious recovery spam. I would change the Refrain rule: a **long rest should reset the remembered spell name/Refrain counter**. Otherwise yesterday's repeated spell can penalize the first cast after sleeping, which is not established by the supplied source.

6. **Conjure Water — QUALIFY.** One active batch, one-hour existence, and no Supply conversion are sufficient economic guards. Reset hydration on **24 elapsed hours**, not “between long rests”; otherwise a character denied a legal long rest for multiple days can receive no further mechanical hydration.

7. **Feather Fall — QUALIFY.** Keep **Action** because both Core placements explicitly say Action. Do not silently convert it to a Reaction. Its usefulness depends on the actual falling procedure. If that procedure resolves every fall completely before another character can take an Action, this spell has a game-interface dependency that must be resolved there rather than by overwriting the spell source.

8. **Unseen Servant — AGREE with one physical clarification.** Bonus Action/shared command, one harmless interaction, no combat body/HP/cover, and dispel termination are sound. Define its notional location/reach explicitly; correction below.

9. **Same-name class cards / aliases — AGREE.** Ordinary spell identity must not grant an equal-named class card. Keeping the 11 uncertain historical aliases blocked is correct.

10. **Common-cost helper scope — AGREE.** Its stated scope is honest: access/gate/common pricing verification, not action legality, class cadence, concentration, targeting, or effect simulation. Do not call its PASS an execution-engine PASS.

### Remaining actionable corrections

1. **Shield — Core range silently discarded.** Both Core entries say **30 feet**; nothing supplied says self-only.  
   **Replace:** `rangeFeet:30`; `targets:"Self or one willing creature you can perceive within 30 feet"`; activation: `"Reaction — when that creature is targeted by an attack roll or Magic Missile, before the attack/damage resolves."`  
   If owner intends self-only, retain range 0 but explicitly record the rejection of Core's 30-foot range.

2. **Predict Movement — same 30-foot narrowing problem.** Core says 30 feet; source does not say self.  
   **Replace:** `rangeFeet:30`; `targets:"One willing creature you can perceive within range"`; otherwise retain current consume-before-roll mechanics.

3. **Resonance Shield — range and components vary by source placement.** Both Core versions have **30-foot range**; rank 0 is V/S while rank 2 is V/S/F. Current self/F-only card changes both.  
   **Replace:** `rangeFeet:30`; `targets:"One willing creature you can perceive within range"`; `components:["V","S"]`; add limitation: `"If the class-specific source placement being used includes F, an existing class casting focus is additionally required."`  
   Keep the chosen 1d4/+1-RP provisional effect.

4. **False Life — Core 30-foot range is silently narrowed to self.** The word “Gain” alone does not conclusively override the Core range.  
   **Replace:** `rangeFeet:30`; `targets:"One willing living creature you can perceive within range"` unless owner explicitly chooses self-only and records that override.

5. **Locate Object — `rangeFeet:1000` conflates casting range with detection radius.** The explicit source effect supplies a **1,000-foot search radius**; the Divination Core entry gives range 0 feet.  
   **Replace:** `rangeFeet:0`; `targets:"Self; one specific familiar object being sought"`; keep `within 1,000 feet` in effect/limitations. Record the conflicting Universal 30-foot placement separately.

6. **Conjure Water — hydration reset anchor.**  
   **Replace:** `"A creature may satisfy its ordinary water need from Conjure Water once per 24 elapsed in-world hours."`  
   Keep one active batch, one-hour lifespan, and no abstract Supply reduction.

7. **Unseen Servant — no physical interaction position is defined.** It has Speed but no body/space/reach, so object interaction range is ambiguous.  
   **Add:** `"The servant has a notional location but occupies no space, blocks no movement, and provides no cover. It may perform its one commanded interaction only on an object within 5 feet of that notional location."`

8. **Message — 25-word cap is unsupported by the supplied sources and resembles an imported external spell assumption.**  
   **Replace effect:** `"Transmit one brief whispered message that could ordinarily be spoken during one Action directly to the target."`  
   Remove the exact 25-word number unless local canon supplies it.

9. **Mental Flicker — source eligibility 'minor creature' disappeared.** Current draft can affect anything.  
   **Replace targets:** `"One non-boss creature you can perceive within 30 feet."`  
   Add design note: `"Non-boss is the provisional operational interpretation of source 'minor creature'; legendary/boss definitions remain governed by encounter data."`

10. **Summon Lesser Skeleton — piercing damage is invented.** Source only says `1d6 melee`.  
    **Replace:** `"one melee attack ... dealing 1d6 bludgeoning, piercing, or slashing damage; choose the physical type when summoned and keep it fixed for that summon."`

11. **Refrain across long rests — persistent remembered spell is mechanically anomalous.**  
    **Replace recovery text:** `"A completed long rest restores RP, clears Dissonance, and resets the remembered spell name and Refrain counter. A short rest clears Dissonance through Retune but does not reset Refrain unless a class feature expressly says so."`

12. **Two malformed target strings should be fixed before machine consumption.**  
    `seal-minor-wound` → `"One living creature you can perceive within 30 feet"`  
    `earthen-grip` → `"One Large-or-smaller creature touching solid ground that you can perceive within 30 feet"`

After those corrections, I would treat the **72-spell starter as integration-ready provisional material** for validator and human-table testing, not canon or balance-approved. The remaining 776 should stay blocked rather than inherit these decisions automatically.