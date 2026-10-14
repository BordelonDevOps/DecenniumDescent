The bounded interface is very close, but I would make **three corrections before closure**. Everything else in the saved text is internally coherent and correctly distinguishes Core/V6 recovery from provisional overlay decisions. Pasted text

1. **Wound-treatment Supply consumption currently changes the adopted Gameplay source without labeling the change.** The source language previously supplied says treatment requires one Supply, but specifically says **Failure consumes the Supply**; the saved overlay now says it is “consumed once regardless of outcome.” Pasted text  
   **Replace with:**
   > Treatment requires a medical kit and one Supply available when treatment begins. Choose the Wound being treated before the check. On Critical Success or Success, the Supply is not consumed. On Failure or Critical Failure, consume the Supply.  
   
   If the owner wants guaranteed consumption on every attempt, that is mechanically reasonable but must be labeled **NEW PROVISIONAL OVERRIDE of the retained Gameplay procedure**, not source-derived.

2. **Do not yet declare the named Core condition `Wounded` to be merely an alias.** You have identified `Wounded` as one of the 13 named Core conditions whose complete operational text is still awaiting the conditions pass. Therefore line 67 makes a relationship decision before that source has been audited. Pasted text  
   **Replace the final sentence with:**
   > These Wound records are the sole source of the Wound-count penalties in this overlay. Do not additionally apply penalties merely because another rule uses the term **Wounded**. The relationship between Wound records and the separately named Core **Wounded** condition remains reserved for the condition audit.

   That prevents double penalties now without prejudging what the condition actually means.

3. **Remove the assertion that Initiative is a Dexterity check from the Injury section.** Initiative calculation is outside this bounded subsystem and should not be fixed incidentally just to resolve Injury overlap. Pasted text  
   **Replace:**
   > `Initiative is a Dexterity check for this overlap; an injury changes future initiative rolls, not an order already established.`
   
   **With:**
   > An Injury penalty affecting Initiative applies only to future Initiative rolls and never retroactively changes an established order. If another Injury also applies to the same Initiative roll under the active Initiative procedure, use only the strongest Injury penalty.

### Everything else verifies

The following can stand as written:

- widened critical ranges still require the attack to meet AC unless expressly stated otherwise;
- task degrees are separated from attacks and saves;
- opposed ties preserve state;
- temporary HP is removed before normal HP;
- the half-max Wound trigger uses **post-temp damage**, clearly labeled provisional;
- Instant Death resolves before Wounds and death failures;
- one damage event produces at most one Wound save;
- pre-event/pre-save Wound count controls Critical-state death;
- 2 → 3 Wounds does not kill; a later failed Wound save starting at 3 does;
- a hit dropping positive HP to zero does not also inflict a same-packet death failure;
- knockout cannot bypass Instant Death or a fatal Wound save;
- Core Unconscious supplies Prone rather than Gameplay inventing it;
- Stable, counter reset, 1d4-hour recovery, monster death behavior and knockout have restored V6 provenance;
- the max-HP-1 Critical healing ceiling handles max HP 1 without trapping the creature at 0;
- Stable recovery and rest share one elapsed clock;
- linked Injuries produce no additional Wounds and disappear with their associated Wound;
- Mobility Trauma and Critical Speed reduction are distinct and may both apply once;
- Critical Failure treatment Strain belongs to the **patient**;
- validator scope is correctly described as reference/state-transition testing rather than a full combat engine. Pasted text

**Disposition: 3 textual corrections remain. After those, I would close the bounded Core-resolution / HP / Wound / death / Injury interface as `REVIEWED` and ready for its reference validation tests—not as full combat completion.**