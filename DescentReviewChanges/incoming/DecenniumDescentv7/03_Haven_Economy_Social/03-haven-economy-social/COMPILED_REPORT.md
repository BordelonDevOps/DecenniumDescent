# Compiled Cursor Multi-Agent Playtest Report

Result files: **120**

## Scenario: HAV-APPRAISAL

### Agent: anti-trafficking-investigator

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- bible_example_gross: 3094
- observed_seed1_gross: 3094
- misprice_abs_mean: 587.15
- appraisal_fail_or_critfail: 11
**Observations**
- Recomputed bible sale formula Final Value = Base x Provenance x Demand x Condition x Urgency; seed1=3094 gp matches extract.
- Across 20 seeds, mean |believed-true| misprice=587.1 gp under appraisal outcome model.
- Patient auction of documented damaged lens matches bible: 4500 x 1.0 x 1.25 x 0.5 x 1.1 = 3094 gp.
- Critical appraisal failure sells as sound/undocumented; buyers later litigate provenance - Claimant of Record exposed.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: artifact-appraiser

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- bible_example_gross: 3094
- observed_seed1_gross: 3094
- misprice_abs_mean: 587.15
- appraisal_fail_or_critfail: 11
**Observations**
- Recomputed bible sale formula Final Value = Base x Provenance x Demand x Condition x Urgency; seed1=3094 gp matches extract.
- Across 20 seeds, mean |believed-true| misprice=587.1 gp under appraisal outcome model.
- Critical failure invents false condition/provenance; error reveals only when material - per appraisal outcomes.
- Patient auction of documented damaged lens matches bible: 4500 x 1.0 x 1.25 x 0.5 x 1.1 = 3094 gp.
- Critical appraisal failure sells as sound/undocumented; buyers later litigate provenance - Claimant of Record exposed.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?
- Is there a published buyer table for 'best current buyer' on critical success?

### Agent: brewer-alchemist

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- bible_example_gross: 3094
- observed_seed1_gross: 3094
- misprice_abs_mean: 587.15
- appraisal_fail_or_critfail: 11
**Observations**
- Recomputed bible sale formula Final Value = Base x Provenance x Demand x Condition x Urgency; seed1=3094 gp matches extract.
- Across 20 seeds, mean |believed-true| misprice=587.1 gp under appraisal outcome model.
- Patient auction of documented damaged lens matches bible: 4500 x 1.0 x 1.25 x 0.5 x 1.1 = 3094 gp.
- Critical appraisal failure sells as sound/undocumented; buyers later litigate provenance - Claimant of Record exposed.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: expedition-quartermaster

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- bible_example_gross: 3094
- observed_seed1_gross: 3094
- misprice_abs_mean: 587.15
- appraisal_fail_or_critfail: 11
**Observations**
- Recomputed bible sale formula Final Value = Base x Provenance x Demand x Condition x Urgency; seed1=3094 gp matches extract.
- Across 20 seeds, mean |believed-true| misprice=587.1 gp under appraisal outcome model.
- Net after example tax + 20% guild share leaves wages/repairs unpaid in formula - settlement step required.
- Patient auction of documented damaged lens matches bible: 4500 x 1.0 x 1.25 x 0.5 x 1.1 = 3094 gp.
- Critical appraisal failure sells as sound/undocumented; buyers later litigate provenance - Claimant of Record exposed.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?
**Recommendations**
- Publish wage/repair line items so Quartermaster can refuse incomplete settlement sheets.

### Agent: faction-broker

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- bible_example_gross: 3094
- observed_seed1_gross: 3094
- misprice_abs_mean: 587.15
- appraisal_fail_or_critfail: 11
- standing_scale_conflict: Loop -5..+5 vs reputation.js Hated/Disliked/Neutral/Liked/Honored
**Observations**
- Recomputed bible sale formula Final Value = Base x Provenance x Demand x Condition x Urgency; seed1=3094 gp matches extract.
- Across 20 seeds, mean |believed-true| misprice=587.1 gp under appraisal outcome model.
- Patient auction of documented damaged lens matches bible: 4500 x 1.0 x 1.25 x 0.5 x 1.1 = 3094 gp.
- Critical appraisal failure sells as sound/undocumented; buyers later litigate provenance - Claimant of Record exposed.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: goblin-banker

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- bible_example_gross: 3094
- observed_seed1_gross: 3094
- misprice_abs_mean: 587.15
- appraisal_fail_or_critfail: 11
**Observations**
- Recomputed bible sale formula Final Value = Base x Provenance x Demand x Condition x Urgency; seed1=3094 gp matches extract.
- Across 20 seeds, mean |believed-true| misprice=587.1 gp under appraisal outcome model.
- Patient auction of documented damaged lens matches bible: 4500 x 1.0 x 1.25 x 0.5 x 1.1 = 3094 gp.
- Critical appraisal failure sells as sound/undocumented; buyers later litigate provenance - Claimant of Record exposed.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: guild-sponsor

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- bible_example_gross: 3094
- observed_seed1_gross: 3094
- misprice_abs_mean: 587.15
- appraisal_fail_or_critfail: 11
**Observations**
- Recomputed bible sale formula Final Value = Base x Provenance x Demand x Condition x Urgency; seed1=3094 gp matches extract.
- Across 20 seeds, mean |believed-true| misprice=587.1 gp under appraisal outcome model.
- Patient auction of documented damaged lens matches bible: 4500 x 1.0 x 1.25 x 0.5 x 1.1 = 3094 gp.
- Critical appraisal failure sells as sound/undocumented; buyers later litigate provenance - Claimant of Record exposed.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: haven-magistrate

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- bible_example_gross: 3094
- observed_seed1_gross: 3094
- misprice_abs_mean: 587.15
- appraisal_fail_or_critfail: 11
**Observations**
- Recomputed bible sale formula Final Value = Base x Provenance x Demand x Condition x Urgency; seed1=3094 gp matches extract.
- Across 20 seeds, mean |believed-true| misprice=587.1 gp under appraisal outcome model.
- Patient auction of documented damaged lens matches bible: 4500 x 1.0 x 1.25 x 0.5 x 1.1 = 3094 gp.
- Critical appraisal failure sells as sound/undocumented; buyers later litigate provenance - Claimant of Record exposed.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?
- Quarantine can force urgency=forced (0.75); need explicit clock tying inspection delay to urgency.

### Agent: labor-organizer

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- bible_example_gross: 3094
- observed_seed1_gross: 3094
- misprice_abs_mean: 587.15
- appraisal_fail_or_critfail: 11
**Observations**
- Recomputed bible sale formula Final Value = Base x Provenance x Demand x Condition x Urgency; seed1=3094 gp matches extract.
- Across 20 seeds, mean |believed-true| misprice=587.1 gp under appraisal outcome model.
- Patient auction of documented damaged lens matches bible: 4500 x 1.0 x 1.25 x 0.5 x 1.1 = 3094 gp.
- Critical appraisal failure sells as sound/undocumented; buyers later litigate provenance - Claimant of Record exposed.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: market-auditor

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- bible_example_gross: 3094
- observed_seed1_gross: 3094
- misprice_abs_mean: 587.15
- appraisal_fail_or_critfail: 11
- auditor_recompute_note: Recomputed all seed settlements in harness; see sim export
**Observations**
- Recomputed bible sale formula Final Value = Base x Provenance x Demand x Condition x Urgency; seed1=3094 gp matches extract.
- Across 20 seeds, mean |believed-true| misprice=587.1 gp under appraisal outcome model.
- Taxes/shares apply after value determination - order verified against section 17.
- Patient auction of documented damaged lens matches bible: 4500 x 1.0 x 1.25 x 0.5 x 1.1 = 3094 gp.
- Critical appraisal failure sells as sound/undocumented; buyers later litigate provenance - Claimant of Record exposed.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?
**Exploits**
- If Directors skip provenance filing, undocumented 0.5 multiplier never applies - infinite soft profit vs RAW.

### Agent: pleasure-house-operator

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- bible_example_gross: 3094
- observed_seed1_gross: 3094
- misprice_abs_mean: 587.15
- appraisal_fail_or_critfail: 11
**Observations**
- Recomputed bible sale formula Final Value = Base x Provenance x Demand x Condition x Urgency; seed1=3094 gp matches extract.
- Across 20 seeds, mean |believed-true| misprice=587.1 gp under appraisal outcome model.
- Patient auction of documented damaged lens matches bible: 4500 x 1.0 x 1.25 x 0.5 x 1.1 = 3094 gp.
- Critical appraisal failure sells as sound/undocumented; buyers later litigate provenance - Claimant of Record exposed.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: smuggler

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- bible_example_gross: 3094
- observed_seed1_gross: 3094
- misprice_abs_mean: 587.15
- appraisal_fail_or_critfail: 11
**Observations**
- Recomputed bible sale formula Final Value = Base x Provenance x Demand x Condition x Urgency; seed1=3094 gp matches extract.
- Across 20 seeds, mean |believed-true| misprice=587.1 gp under appraisal outcome model.
- Patient auction of documented damaged lens matches bible: 4500 x 1.0 x 1.25 x 0.5 x 1.1 = 3094 gp.
- Critical appraisal failure sells as sound/undocumented; buyers later litigate provenance - Claimant of Record exposed.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

## Scenario: HAV-BREWING

### Agent: anti-trafficking-investigator

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- mean_profit: 44.88
- unlicensed_events: 1
**Observations**
- Brewery expansion mean profit 44.88 gp under 40% cost assumption; unlicensed=1.
- Small beer high volume / tiny margin; expansion needs Makers' Quarter space licenses (unpublished fee).
- Tier 4+ mead without license triggers magistrate fine assumption - profit erased.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: artifact-appraiser

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- mean_profit: 44.88
- unlicensed_events: 1
**Observations**
- Brewery expansion mean profit 44.88 gp under 40% cost assumption; unlicensed=1.
- Small beer high volume / tiny margin; expansion needs Makers' Quarter space licenses (unpublished fee).
- Tier 4+ mead without license triggers magistrate fine assumption - profit erased.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: brewer-alchemist

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- mean_profit: 44.88
- unlicensed_events: 1
**Observations**
- Brewery expansion mean profit 44.88 gp under 40% cost assumption; unlicensed=1.
- Small beer high volume / tiny margin; expansion needs Makers' Quarter space licenses (unpublished fee).
- Tier 4+ mead without license triggers magistrate fine assumption - profit erased.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?
- What are Makers' Quarter production costs, spoilage clocks, and license fees by brew tier?

### Agent: expedition-quartermaster

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- mean_profit: 44.88
- unlicensed_events: 1
**Observations**
- Brewery expansion mean profit 44.88 gp under 40% cost assumption; unlicensed=1.
- Small beer high volume / tiny margin; expansion needs Makers' Quarter space licenses (unpublished fee).
- Tier 4+ mead without license triggers magistrate fine assumption - profit erased.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: faction-broker

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- mean_profit: 44.88
- unlicensed_events: 1
- standing_scale_conflict: Loop -5..+5 vs reputation.js Hated/Disliked/Neutral/Liked/Honored
**Observations**
- Brewery expansion mean profit 44.88 gp under 40% cost assumption; unlicensed=1.
- Small beer high volume / tiny margin; expansion needs Makers' Quarter space licenses (unpublished fee).
- Tier 4+ mead without license triggers magistrate fine assumption - profit erased.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: goblin-banker

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- mean_profit: 44.88
- unlicensed_events: 1
**Observations**
- Brewery expansion mean profit 44.88 gp under 40% cost assumption; unlicensed=1.
- Small beer high volume / tiny margin; expansion needs Makers' Quarter space licenses (unpublished fee).
- Tier 4+ mead without license triggers magistrate fine assumption - profit erased.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: guild-sponsor

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- mean_profit: 44.88
- unlicensed_events: 1
**Observations**
- Brewery expansion mean profit 44.88 gp under 40% cost assumption; unlicensed=1.
- Small beer high volume / tiny margin; expansion needs Makers' Quarter space licenses (unpublished fee).
- Tier 4+ mead without license triggers magistrate fine assumption - profit erased.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: haven-magistrate

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- mean_profit: 44.88
- unlicensed_events: 1
**Observations**
- Brewery expansion mean profit 44.88 gp under 40% cost assumption; unlicensed=1.
- Small beer high volume / tiny margin; expansion needs Makers' Quarter space licenses (unpublished fee).
- Tier 4+ mead without license triggers magistrate fine assumption - profit erased.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: labor-organizer

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- mean_profit: 44.88
- unlicensed_events: 1
**Observations**
- Brewery expansion mean profit 44.88 gp under 40% cost assumption; unlicensed=1.
- Small beer high volume / tiny margin; expansion needs Makers' Quarter space licenses (unpublished fee).
- Tier 4+ mead without license triggers magistrate fine assumption - profit erased.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: market-auditor

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- mean_profit: 44.88
- unlicensed_events: 1
- auditor_recompute_note: Recomputed all seed settlements in harness; see sim export
**Observations**
- Brewery expansion mean profit 44.88 gp under 40% cost assumption; unlicensed=1.
- Listed brew prices (cp-gp) cannot replace expedition cargo income - no infinite brew profit observed at RAW list prices.
- Small beer high volume / tiny margin; expansion needs Makers' Quarter space licenses (unpublished fee).
- Tier 4+ mead without license triggers magistrate fine assumption - profit erased.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: pleasure-house-operator

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- mean_profit: 44.88
- unlicensed_events: 1
**Observations**
- Brewery expansion mean profit 44.88 gp under 40% cost assumption; unlicensed=1.
- Small beer high volume / tiny margin; expansion needs Makers' Quarter space licenses (unpublished fee).
- Tier 4+ mead without license triggers magistrate fine assumption - profit erased.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: smuggler

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- mean_profit: 44.88
- unlicensed_events: 1
**Observations**
- Brewery expansion mean profit 44.88 gp under 40% cost assumption; unlicensed=1.
- Small beer high volume / tiny margin; expansion needs Makers' Quarter space licenses (unpublished fee).
- Tier 4+ mead without license triggers magistrate fine assumption - profit erased.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

## Scenario: HAV-COIN

### Agent: anti-trafficking-investigator

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- mean_loss_vs_face: 202.02
- undetected_cf_rate: 0.55
**Observations**
- Iron Ledger scenario: mean loss vs face 202.0 gp; undetected counterfeit rate 0.55 under assumed DCs.
- haven.json names reminting/shaved-coin detection but publishes no fees, DCs, or remint yield.
- Iron Ledger Houses receive mixed batch; shaved coin detected; remint fee unpublished - table stalls.
- Counterfeit slips assay; later charged back to expedition renown - bankers not uniformly corrupt.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: artifact-appraiser

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- mean_loss_vs_face: 202.02
- undetected_cf_rate: 0.55
**Observations**
- Iron Ledger scenario: mean loss vs face 202.0 gp; undetected counterfeit rate 0.55 under assumed DCs.
- haven.json names reminting/shaved-coin detection but publishes no fees, DCs, or remint yield.
- Iron Ledger Houses receive mixed batch; shaved coin detected; remint fee unpublished - table stalls.
- Counterfeit slips assay; later charged back to expedition renown - bankers not uniformly corrupt.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: brewer-alchemist

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- mean_loss_vs_face: 202.02
- undetected_cf_rate: 0.55
**Observations**
- Iron Ledger scenario: mean loss vs face 202.0 gp; undetected counterfeit rate 0.55 under assumed DCs.
- haven.json names reminting/shaved-coin detection but publishes no fees, DCs, or remint yield.
- Iron Ledger Houses receive mixed batch; shaved coin detected; remint fee unpublished - table stalls.
- Counterfeit slips assay; later charged back to expedition renown - bankers not uniformly corrupt.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: expedition-quartermaster

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- mean_loss_vs_face: 202.02
- undetected_cf_rate: 0.55
**Observations**
- Iron Ledger scenario: mean loss vs face 202.0 gp; undetected counterfeit rate 0.55 under assumed DCs.
- haven.json names reminting/shaved-coin detection but publishes no fees, DCs, or remint yield.
- Iron Ledger Houses receive mixed batch; shaved coin detected; remint fee unpublished - table stalls.
- Counterfeit slips assay; later charged back to expedition renown - bankers not uniformly corrupt.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: faction-broker

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- mean_loss_vs_face: 202.02
- undetected_cf_rate: 0.55
- standing_scale_conflict: Loop -5..+5 vs reputation.js Hated/Disliked/Neutral/Liked/Honored
**Observations**
- Iron Ledger scenario: mean loss vs face 202.0 gp; undetected counterfeit rate 0.55 under assumed DCs.
- haven.json names reminting/shaved-coin detection but publishes no fees, DCs, or remint yield.
- Iron Ledger Houses receive mixed batch; shaved coin detected; remint fee unpublished - table stalls.
- Counterfeit slips assay; later charged back to expedition renown - bankers not uniformly corrupt.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: goblin-banker

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- mean_loss_vs_face: 202.02
- undetected_cf_rate: 0.55
**Observations**
- Iron Ledger scenario: mean loss vs face 202.0 gp; undetected counterfeit rate 0.55 under assumed DCs.
- haven.json names reminting/shaved-coin detection but publishes no fees, DCs, or remint yield.
- Must not assume every goblin knowingly corrupt; honest assay still needs numeric remint schedule.
- Iron Ledger Houses receive mixed batch; shaved coin detected; remint fee unpublished - table stalls.
- Counterfeit slips assay; later charged back to expedition renown - bankers not uniformly corrupt.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?
- Publish assay DC by adulteration %, remint fee, and collateral rules for Iron Ledger Houses.

### Agent: guild-sponsor

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- mean_loss_vs_face: 202.02
- undetected_cf_rate: 0.55
**Observations**
- Iron Ledger scenario: mean loss vs face 202.0 gp; undetected counterfeit rate 0.55 under assumed DCs.
- haven.json names reminting/shaved-coin detection but publishes no fees, DCs, or remint yield.
- Iron Ledger Houses receive mixed batch; shaved coin detected; remint fee unpublished - table stalls.
- Counterfeit slips assay; later charged back to expedition renown - bankers not uniformly corrupt.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: haven-magistrate

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- mean_loss_vs_face: 202.02
- undetected_cf_rate: 0.55
**Observations**
- Iron Ledger scenario: mean loss vs face 202.0 gp; undetected counterfeit rate 0.55 under assumed DCs.
- haven.json names reminting/shaved-coin detection but publishes no fees, DCs, or remint yield.
- Iron Ledger Houses receive mixed batch; shaved coin detected; remint fee unpublished - table stalls.
- Counterfeit slips assay; later charged back to expedition renown - bankers not uniformly corrupt.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: labor-organizer

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- mean_loss_vs_face: 202.02
- undetected_cf_rate: 0.55
**Observations**
- Iron Ledger scenario: mean loss vs face 202.0 gp; undetected counterfeit rate 0.55 under assumed DCs.
- haven.json names reminting/shaved-coin detection but publishes no fees, DCs, or remint yield.
- Iron Ledger Houses receive mixed batch; shaved coin detected; remint fee unpublished - table stalls.
- Counterfeit slips assay; later charged back to expedition renown - bankers not uniformly corrupt.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: market-auditor

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- mean_loss_vs_face: 202.02
- undetected_cf_rate: 0.55
- auditor_recompute_note: Recomputed all seed settlements in harness; see sim export
**Observations**
- Iron Ledger scenario: mean loss vs face 202.0 gp; undetected counterfeit rate 0.55 under assumed DCs.
- haven.json names reminting/shaved-coin detection but publishes no fees, DCs, or remint yield.
- Iron Ledger Houses receive mixed batch; shaved coin detected; remint fee unpublished - table stalls.
- Counterfeit slips assay; later charged back to expedition renown - bankers not uniformly corrupt.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?
**Exploits**
- Without remint fees, players can treat shaved coin at face indefinitely - infinite soft profit.

### Agent: pleasure-house-operator

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- mean_loss_vs_face: 202.02
- undetected_cf_rate: 0.55
**Observations**
- Iron Ledger scenario: mean loss vs face 202.0 gp; undetected counterfeit rate 0.55 under assumed DCs.
- haven.json names reminting/shaved-coin detection but publishes no fees, DCs, or remint yield.
- Iron Ledger Houses receive mixed batch; shaved coin detected; remint fee unpublished - table stalls.
- Counterfeit slips assay; later charged back to expedition renown - bankers not uniformly corrupt.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: smuggler

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- mean_loss_vs_face: 202.02
- undetected_cf_rate: 0.55
**Observations**
- Iron Ledger scenario: mean loss vs face 202.0 gp; undetected counterfeit rate 0.55 under assumed DCs.
- haven.json names reminting/shaved-coin detection but publishes no fees, DCs, or remint yield.
- Iron Ledger Houses receive mixed batch; shaved coin detected; remint fee unpublished - table stalls.
- Counterfeit slips assay; later charged back to expedition renown - bankers not uniformly corrupt.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

## Scenario: HAV-LABOR

### Agent: anti-trafficking-investigator

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- emancipation_rate: 0.15
- rescue_rate: 0.2
- law_rate: 0.2
**Observations**
- Porter debt: emancipation 15%, rescue 20%, law 20% under assumed wage/interest.
- Labor debt != trafficking but can convert; keep distinct claim types on Chain Market.
- Porter debt advance + interest exceeds earned wages in most seeds - emancipation rare without rescue.
- Strike triggers merchant standing loss and occasional law intervention.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: artifact-appraiser

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- emancipation_rate: 0.15
- rescue_rate: 0.2
- law_rate: 0.2
**Observations**
- Porter debt: emancipation 15%, rescue 20%, law 20% under assumed wage/interest.
- Porter debt advance + interest exceeds earned wages in most seeds - emancipation rare without rescue.
- Strike triggers merchant standing loss and occasional law intervention.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: brewer-alchemist

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- emancipation_rate: 0.15
- rescue_rate: 0.2
- law_rate: 0.2
**Observations**
- Porter debt: emancipation 15%, rescue 20%, law 20% under assumed wage/interest.
- Porter debt advance + interest exceeds earned wages in most seeds - emancipation rare without rescue.
- Strike triggers merchant standing loss and occasional law intervention.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: expedition-quartermaster

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- emancipation_rate: 0.15
- rescue_rate: 0.2
- law_rate: 0.2
**Observations**
- Porter debt: emancipation 15%, rescue 20%, law 20% under assumed wage/interest.
- Porter debt advance + interest exceeds earned wages in most seeds - emancipation rare without rescue.
- Strike triggers merchant standing loss and occasional law intervention.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: faction-broker

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- emancipation_rate: 0.15
- rescue_rate: 0.2
- law_rate: 0.2
- standing_scale_conflict: Loop -5..+5 vs reputation.js Hated/Disliked/Neutral/Liked/Honored
**Observations**
- Porter debt: emancipation 15%, rescue 20%, law 20% under assumed wage/interest.
- Porter debt advance + interest exceeds earned wages in most seeds - emancipation rare without rescue.
- Strike triggers merchant standing loss and occasional law intervention.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: goblin-banker

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- emancipation_rate: 0.15
- rescue_rate: 0.2
- law_rate: 0.2
**Observations**
- Porter debt: emancipation 15%, rescue 20%, law 20% under assumed wage/interest.
- Porter debt advance + interest exceeds earned wages in most seeds - emancipation rare without rescue.
- Strike triggers merchant standing loss and occasional law intervention.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: guild-sponsor

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- emancipation_rate: 0.15
- rescue_rate: 0.2
- law_rate: 0.2
**Observations**
- Porter debt: emancipation 15%, rescue 20%, law 20% under assumed wage/interest.
- Unpaid porters reduce convoy Capacity - sponsor share on paper means nothing if Load collapses next descent.
- Porter debt advance + interest exceeds earned wages in most seeds - emancipation rare without rescue.
- Strike triggers merchant standing loss and occasional law intervention.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: haven-magistrate

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- emancipation_rate: 0.15
- rescue_rate: 0.2
- law_rate: 0.2
**Observations**
- Porter debt: emancipation 15%, rescue 20%, law 20% under assumed wage/interest.
- Porter debt advance + interest exceeds earned wages in most seeds - emancipation rare without rescue.
- Strike triggers merchant standing loss and occasional law intervention.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: labor-organizer

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- emancipation_rate: 0.15
- rescue_rate: 0.2
- law_rate: 0.2
**Observations**
- Porter debt: emancipation 15%, rescue 20%, law 20% under assumed wage/interest.
- Debt bondage frequently traps porters when interest is high - resistance/rescue/law paths are necessary, not optional color.
- Porter debt advance + interest exceeds earned wages in most seeds - emancipation rare without rescue.
- Strike triggers merchant standing loss and occasional law intervention.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?
- Publish fair wage, max advance interest, strike resolution, and emancipation buyout formula.

### Agent: market-auditor

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- emancipation_rate: 0.15
- rescue_rate: 0.2
- law_rate: 0.2
- auditor_recompute_note: Recomputed all seed settlements in harness; see sim export
**Observations**
- Porter debt: emancipation 15%, rescue 20%, law 20% under assumed wage/interest.
- Porter debt advance + interest exceeds earned wages in most seeds - emancipation rare without rescue.
- Strike triggers merchant standing loss and occasional law intervention.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: pleasure-house-operator

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- emancipation_rate: 0.15
- rescue_rate: 0.2
- law_rate: 0.2
**Observations**
- Porter debt: emancipation 15%, rescue 20%, law 20% under assumed wage/interest.
- Porter debt advance + interest exceeds earned wages in most seeds - emancipation rare without rescue.
- Strike triggers merchant standing loss and occasional law intervention.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: smuggler

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- emancipation_rate: 0.15
- rescue_rate: 0.2
- law_rate: 0.2
**Observations**
- Porter debt: emancipation 15%, rescue 20%, law 20% under assumed wage/interest.
- Porter debt advance + interest exceeds earned wages in most seeds - emancipation rare without rescue.
- Strike triggers merchant standing loss and occasional law intervention.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

## Scenario: HAV-MARKET-SHOCK

### Agent: anti-trafficking-investigator

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- mean_collapse_pct: 0.55
- extraction_still_relevant_rate: 1.0
- tier2_materials_sampled: 30
**Observations**
- Tier II influx: mean price collapse 55%; deeper extraction still beats glut dump in 100% seeds.
- Tier II influx flips demand sought->glutted and urgency toward forced sale - price collapse observed.
- Crafting hold (assumed +40%) softens shock but deeper sought extraction still wins in most seeds.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: artifact-appraiser

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- mean_collapse_pct: 0.55
- extraction_still_relevant_rate: 1.0
- tier2_materials_sampled: 30
**Observations**
- Tier II influx: mean price collapse 55%; deeper extraction still beats glut dump in 100% seeds.
- Tier II influx flips demand sought->glutted and urgency toward forced sale - price collapse observed.
- Crafting hold (assumed +40%) softens shock but deeper sought extraction still wins in most seeds.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: brewer-alchemist

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- mean_collapse_pct: 0.55
- extraction_still_relevant_rate: 1.0
- tier2_materials_sampled: 30
**Observations**
- Tier II influx: mean price collapse 55%; deeper extraction still beats glut dump in 100% seeds.
- Tier II influx flips demand sought->glutted and urgency toward forced sale - price collapse observed.
- Crafting hold (assumed +40%) softens shock but deeper sought extraction still wins in most seeds.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: expedition-quartermaster

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- mean_collapse_pct: 0.55
- extraction_still_relevant_rate: 1.0
- tier2_materials_sampled: 30
**Observations**
- Tier II influx: mean price collapse 55%; deeper extraction still beats glut dump in 100% seeds.
- Shock pushes differentiated/Gate-Sealed cargo and crafting holds - extraction remains meaningful.
- Tier II influx flips demand sought->glutted and urgency toward forced sale - price collapse observed.
- Crafting hold (assumed +40%) softens shock but deeper sought extraction still wins in most seeds.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: faction-broker

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- mean_collapse_pct: 0.55
- extraction_still_relevant_rate: 1.0
- tier2_materials_sampled: 30
- standing_scale_conflict: Loop -5..+5 vs reputation.js Hated/Disliked/Neutral/Liked/Honored
**Observations**
- Tier II influx: mean price collapse 55%; deeper extraction still beats glut dump in 100% seeds.
- Tier II influx flips demand sought->glutted and urgency toward forced sale - price collapse observed.
- Crafting hold (assumed +40%) softens shock but deeper sought extraction still wins in most seeds.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?
**Recommendations**
- Record economic shocks on Cycle Record (Loop section 20) for pack 04 continuity.

### Agent: goblin-banker

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- mean_collapse_pct: 0.55
- extraction_still_relevant_rate: 1.0
- tier2_materials_sampled: 30
**Observations**
- Tier II influx: mean price collapse 55%; deeper extraction still beats glut dump in 100% seeds.
- Tier II influx flips demand sought->glutted and urgency toward forced sale - price collapse observed.
- Crafting hold (assumed +40%) softens shock but deeper sought extraction still wins in most seeds.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: guild-sponsor

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- mean_collapse_pct: 0.55
- extraction_still_relevant_rate: 1.0
- tier2_materials_sampled: 30
**Observations**
- Tier II influx: mean price collapse 55%; deeper extraction still beats glut dump in 100% seeds.
- Tier II influx flips demand sought->glutted and urgency toward forced sale - price collapse observed.
- Crafting hold (assumed +40%) softens shock but deeper sought extraction still wins in most seeds.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: haven-magistrate

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- mean_collapse_pct: 0.55
- extraction_still_relevant_rate: 1.0
- tier2_materials_sampled: 30
**Observations**
- Tier II influx: mean price collapse 55%; deeper extraction still beats glut dump in 100% seeds.
- Tier II influx flips demand sought->glutted and urgency toward forced sale - price collapse observed.
- Crafting hold (assumed +40%) softens shock but deeper sought extraction still wins in most seeds.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: labor-organizer

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- mean_collapse_pct: 0.55
- extraction_still_relevant_rate: 1.0
- tier2_materials_sampled: 30
**Observations**
- Tier II influx: mean price collapse 55%; deeper extraction still beats glut dump in 100% seeds.
- Tier II influx flips demand sought->glutted and urgency toward forced sale - price collapse observed.
- Crafting hold (assumed +40%) softens shock but deeper sought extraction still wins in most seeds.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: market-auditor

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- mean_collapse_pct: 0.55
- extraction_still_relevant_rate: 1.0
- tier2_materials_sampled: 30
- auditor_recompute_note: Recomputed all seed settlements in harness; see sim export
**Observations**
- Tier II influx: mean price collapse 55%; deeper extraction still beats glut dump in 100% seeds.
- Demand glutted 0.75 x forced 0.75 stacks to 0.5625 vs sought x normal 1.25 - RAW multipliers create sharp crash.
- Tier II influx flips demand sought->glutted and urgency toward forced sale - price collapse observed.
- Crafting hold (assumed +40%) softens shock but deeper sought extraction still wins in most seeds.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?
- Many crafting materials lack gp baseValue - market shock math needs explicit Haven commodity prices.

### Agent: pleasure-house-operator

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- mean_collapse_pct: 0.55
- extraction_still_relevant_rate: 1.0
- tier2_materials_sampled: 30
**Observations**
- Tier II influx: mean price collapse 55%; deeper extraction still beats glut dump in 100% seeds.
- Tier II influx flips demand sought->glutted and urgency toward forced sale - price collapse observed.
- Crafting hold (assumed +40%) softens shock but deeper sought extraction still wins in most seeds.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: smuggler

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- mean_collapse_pct: 0.55
- extraction_still_relevant_rate: 1.0
- tier2_materials_sampled: 30
**Observations**
- Tier II influx: mean price collapse 55%; deeper extraction still beats glut dump in 100% seeds.
- Tier II influx flips demand sought->glutted and urgency toward forced sale - price collapse observed.
- Crafting hold (assumed +40%) softens shock but deeper sought extraction still wins in most seeds.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

## Scenario: HAV-PLEASURE

### Agent: anti-trafficking-investigator

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- blackmail_success_rate: 0.05
**Observations**
- Pleasure house: blackmail success 5% when protection fails; trafficking conflation=0 by design.
- Operator cooperation useful for anti-trafficking intel when houses are consensual and protected.
- Consensual house: worker share paid; information tips improve faction access.
- Blackmail attempt blocked by worker protection policy - operator liability.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: artifact-appraiser

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- blackmail_success_rate: 0.05
**Observations**
- Pleasure house: blackmail success 5% when protection fails; trafficking conflation=0 by design.
- Consensual house: worker share paid; information tips improve faction access.
- Blackmail attempt blocked by worker protection policy - operator liability.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: brewer-alchemist

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- blackmail_success_rate: 0.05
**Observations**
- Pleasure house: blackmail success 5% when protection fails; trafficking conflation=0 by design.
- Consensual house: worker share paid; information tips improve faction access.
- Blackmail attempt blocked by worker protection policy - operator liability.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: expedition-quartermaster

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- blackmail_success_rate: 0.05
**Observations**
- Pleasure house: blackmail success 5% when protection fails; trafficking conflation=0 by design.
- Consensual house: worker share paid; information tips improve faction access.
- Blackmail attempt blocked by worker protection policy - operator liability.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: faction-broker

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- blackmail_success_rate: 0.05
- standing_scale_conflict: Loop -5..+5 vs reputation.js Hated/Disliked/Neutral/Liked/Honored
**Observations**
- Pleasure house: blackmail success 5% when protection fails; trafficking conflation=0 by design.
- Info tips can grant +1 standing - must respect +/-2 per-scene cap from Loop section 18.
- Consensual house: worker share paid; information tips improve faction access.
- Blackmail attempt blocked by worker protection policy - operator liability.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: goblin-banker

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- blackmail_success_rate: 0.05
**Observations**
- Pleasure house: blackmail success 5% when protection fails; trafficking conflation=0 by design.
- Consensual house: worker share paid; information tips improve faction access.
- Blackmail attempt blocked by worker protection policy - operator liability.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: guild-sponsor

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- blackmail_success_rate: 0.05
**Observations**
- Pleasure house: blackmail success 5% when protection fails; trafficking conflation=0 by design.
- Consensual house: worker share paid; information tips improve faction access.
- Blackmail attempt blocked by worker protection policy - operator liability.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: haven-magistrate

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- blackmail_success_rate: 0.05
**Observations**
- Pleasure house: blackmail success 5% when protection fails; trafficking conflation=0 by design.
- Consensual house: worker share paid; information tips improve faction access.
- Blackmail attempt blocked by worker protection policy - operator liability.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: labor-organizer

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- blackmail_success_rate: 0.05
**Observations**
- Pleasure house: blackmail success 5% when protection fails; trafficking conflation=0 by design.
- Consensual house: worker share paid; information tips improve faction access.
- Blackmail attempt blocked by worker protection policy - operator liability.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: market-auditor

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- blackmail_success_rate: 0.05
- auditor_recompute_note: Recomputed all seed settlements in harness; see sim export
**Observations**
- Pleasure house: blackmail success 5% when protection fails; trafficking conflation=0 by design.
- Consensual house: worker share paid; information tips improve faction access.
- Blackmail attempt blocked by worker protection policy - operator liability.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: pleasure-house-operator

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- blackmail_success_rate: 0.05
**Observations**
- Pleasure house: blackmail success 5% when protection fails; trafficking conflation=0 by design.
- Worker share and refusal rights modeled as agency; blackmail flagged as crime not balanced income.
- Consensual house: worker share paid; information tips improve faction access.
- Blackmail attempt blocked by worker protection policy - operator liability.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?
- Publish Low Lantern patronage, information brokerage, and worker-protection license rules.

### Agent: smuggler

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- blackmail_success_rate: 0.05
**Observations**
- Pleasure house: blackmail success 5% when protection fails; trafficking conflation=0 by design.
- Consensual house: worker share paid; information tips improve faction access.
- Blackmail attempt blocked by worker protection policy - operator liability.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

## Scenario: HAV-SMUGGLE

### Agent: anti-trafficking-investigator

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- smuggle_beats_legal_rate: 0.0
- catch_rate_observed: 0.15
**Observations**
- Smuggle beat legal net in 0% of seeds; catch rate 15% under Director risk model.
- Undercity route skips tax but undocumented x forced sale + bribes rarely beat documented legal net in 20 seeds.
- Caught smuggle: cargo partial loss + standing -2; extraction risk not bypassed - crime is not free.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: artifact-appraiser

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- smuggle_beats_legal_rate: 0.0
- catch_rate_observed: 0.15
**Observations**
- Smuggle beat legal net in 0% of seeds; catch rate 15% under Director risk model.
- Undercity route skips tax but undocumented x forced sale + bribes rarely beat documented legal net in 20 seeds.
- Caught smuggle: cargo partial loss + standing -2; extraction risk not bypassed - crime is not free.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: brewer-alchemist

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- smuggle_beats_legal_rate: 0.0
- catch_rate_observed: 0.15
**Observations**
- Smuggle beat legal net in 0% of seeds; catch rate 15% under Director risk model.
- Undercity route skips tax but undocumented x forced sale + bribes rarely beat documented legal net in 20 seeds.
- Caught smuggle: cargo partial loss + standing -2; extraction risk not bypassed - crime is not free.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: expedition-quartermaster

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- smuggle_beats_legal_rate: 0.0
- catch_rate_observed: 0.15
**Observations**
- Smuggle beat legal net in 0% of seeds; catch rate 15% under Director risk model.
- Undercity route skips tax but undocumented x forced sale + bribes rarely beat documented legal net in 20 seeds.
- Caught smuggle: cargo partial loss + standing -2; extraction risk not bypassed - crime is not free.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: faction-broker

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- smuggle_beats_legal_rate: 0.0
- catch_rate_observed: 0.15
- standing_scale_conflict: Loop -5..+5 vs reputation.js Hated/Disliked/Neutral/Liked/Honored
**Observations**
- Smuggle beat legal net in 0% of seeds; catch rate 15% under Director risk model.
- Standing deltas (-1/-2) matter under Loop scale; map them onto reputation.js factions (underworld, law-enforcement).
- Undercity route skips tax but undocumented x forced sale + bribes rarely beat documented legal net in 20 seeds.
- Caught smuggle: cargo partial loss + standing -2; extraction risk not bypassed - crime is not free.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: goblin-banker

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- smuggle_beats_legal_rate: 0.0
- catch_rate_observed: 0.15
**Observations**
- Smuggle beat legal net in 0% of seeds; catch rate 15% under Director risk model.
- Undercity route skips tax but undocumented x forced sale + bribes rarely beat documented legal net in 20 seeds.
- Caught smuggle: cargo partial loss + standing -2; extraction risk not bypassed - crime is not free.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: guild-sponsor

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- smuggle_beats_legal_rate: 0.0
- catch_rate_observed: 0.15
**Observations**
- Smuggle beat legal net in 0% of seeds; catch rate 15% under Director risk model.
- Undercity route skips tax but undocumented x forced sale + bribes rarely beat documented legal net in 20 seeds.
- Caught smuggle: cargo partial loss + standing -2; extraction risk not bypassed - crime is not free.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: haven-magistrate

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- smuggle_beats_legal_rate: 0.0
- catch_rate_observed: 0.15
**Observations**
- Smuggle beat legal net in 0% of seeds; catch rate 15% under Director risk model.
- Undercity route skips tax but undocumented x forced sale + bribes rarely beat documented legal net in 20 seeds.
- Caught smuggle: cargo partial loss + standing -2; extraction risk not bypassed - crime is not free.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?
**Recommendations**
- Publish Underways seizure table + bribery as criminal procedure with standing costs.

### Agent: labor-organizer

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- smuggle_beats_legal_rate: 0.0
- catch_rate_observed: 0.15
**Observations**
- Smuggle beat legal net in 0% of seeds; catch rate 15% under Director risk model.
- Undercity route skips tax but undocumented x forced sale + bribes rarely beat documented legal net in 20 seeds.
- Caught smuggle: cargo partial loss + standing -2; extraction risk not bypassed - crime is not free.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: market-auditor

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- smuggle_beats_legal_rate: 0.0
- catch_rate_observed: 0.15
- auditor_recompute_note: Recomputed all seed settlements in harness; see sim export
**Observations**
- Smuggle beat legal net in 0% of seeds; catch rate 15% under Director risk model.
- Undercity route skips tax but undocumented x forced sale + bribes rarely beat documented legal net in 20 seeds.
- Caught smuggle: cargo partial loss + standing -2; extraction risk not bypassed - crime is not free.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: pleasure-house-operator

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- smuggle_beats_legal_rate: 0.0
- catch_rate_observed: 0.15
**Observations**
- Smuggle beat legal net in 0% of seeds; catch rate 15% under Director risk model.
- Undercity route skips tax but undocumented x forced sale + bribes rarely beat documented legal net in 20 seeds.
- Caught smuggle: cargo partial loss + standing -2; extraction risk not bypassed - crime is not free.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: smuggler

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- smuggle_beats_legal_rate: 0.0
- catch_rate_observed: 0.15
**Observations**
- Smuggle beat legal net in 0% of seeds; catch rate 15% under Director risk model.
- Undercity route still requires extracted cargo - does not make dungeon extraction irrelevant.
- Under current assumptions smuggling does not dominate legal sale; risk table still unpublished.
- Undercity route skips tax but undocumented x forced sale + bribes rarely beat documented legal net in 20 seeds.
- Caught smuggle: cargo partial loss + standing -2; extraction risk not bypassed - crime is not free.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?
**Exploits**
- If catch rate house-ruled to ~0 and standing hits ignored, smuggling can dominate legal guild path.

## Scenario: HAV-SPONSOR

### Agent: anti-trafficking-investigator

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- best_sponsor_counts_gp_only: {'self_funded': 19, 'noble_temple': 1}
- best_sponsor_multifactor_counts: {'sovereign': 2, 'self_funded': 17, 'noble_temple': 1}
- dominant_always_gp_only: False
- dominant_always_multifactor: False
**Observations**
- Gp-only best counts: {'self_funded': 19, 'noble_temple': 1} (dominant=False); multifactor counts: {'sovereign': 2, 'self_funded': 17, 'noble_temple': 1} (dominant=False).
- Gp-only scoring often crowns self-funded because share % dominates weak loan friction.
- When seizure risk + appraisal access + political cover are valued, multifactor picks diversify.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: artifact-appraiser

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- best_sponsor_counts_gp_only: {'self_funded': 19, 'noble_temple': 1}
- best_sponsor_multifactor_counts: {'sovereign': 2, 'self_funded': 17, 'noble_temple': 1}
- dominant_always_gp_only: False
- dominant_always_multifactor: False
**Observations**
- Gp-only best counts: {'self_funded': 19, 'noble_temple': 1} (dominant=False); multifactor counts: {'sovereign': 2, 'self_funded': 17, 'noble_temple': 1} (dominant=False).
- Gp-only scoring often crowns self-funded because share % dominates weak loan friction.
- When seizure risk + appraisal access + political cover are valued, multifactor picks diversify.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: brewer-alchemist

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- best_sponsor_counts_gp_only: {'self_funded': 19, 'noble_temple': 1}
- best_sponsor_multifactor_counts: {'sovereign': 2, 'self_funded': 17, 'noble_temple': 1}
- dominant_always_gp_only: False
- dominant_always_multifactor: False
**Observations**
- Gp-only best counts: {'self_funded': 19, 'noble_temple': 1} (dominant=False); multifactor counts: {'sovereign': 2, 'self_funded': 17, 'noble_temple': 1} (dominant=False).
- Gp-only scoring often crowns self-funded because share % dominates weak loan friction.
- When seizure risk + appraisal access + political cover are valued, multifactor picks diversify.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: expedition-quartermaster

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- best_sponsor_counts_gp_only: {'self_funded': 19, 'noble_temple': 1}
- best_sponsor_multifactor_counts: {'sovereign': 2, 'self_funded': 17, 'noble_temple': 1}
- dominant_always_gp_only: False
- dominant_always_multifactor: False
**Observations**
- Gp-only best counts: {'self_funded': 19, 'noble_temple': 1} (dominant=False); multifactor counts: {'sovereign': 2, 'self_funded': 17, 'noble_temple': 1} (dominant=False).
- Observed: naive treasury math makes self-funded dominant; RAW up-front support lacks priced benefits.
- Gp-only scoring often crowns self-funded because share % dominates weak loan friction.
- When seizure risk + appraisal access + political cover are valued, multifactor picks diversify.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?
**Exploits**
- Gp-only players can treat self-funded as always correct unless capital gates are harsh.
**Recommendations**
- Price appraisal access, seizure cover, and capital in gp-equivalent or standing so sponsor choice stays meaningful.

### Agent: faction-broker

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- best_sponsor_counts_gp_only: {'self_funded': 19, 'noble_temple': 1}
- best_sponsor_multifactor_counts: {'sovereign': 2, 'self_funded': 17, 'noble_temple': 1}
- dominant_always_gp_only: False
- dominant_always_multifactor: False
- standing_scale_conflict: Loop -5..+5 vs reputation.js Hated/Disliked/Neutral/Liked/Honored
**Observations**
- Gp-only best counts: {'self_funded': 19, 'noble_temple': 1} (dominant=False); multifactor counts: {'sovereign': 2, 'self_funded': 17, 'noble_temple': 1} (dominant=False).
- Noble/temple and sovereign buy political cover - standing access not captured in gp-only comparison.
- Gp-only scoring often crowns self-funded because share % dominates weak loan friction.
- When seizure risk + appraisal access + political cover are valued, multifactor picks diversify.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?
- How much standing does political cover grant, and is it inside the +/-2 per-scene cap?

### Agent: goblin-banker

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- best_sponsor_counts_gp_only: {'self_funded': 19, 'noble_temple': 1}
- best_sponsor_multifactor_counts: {'sovereign': 2, 'self_funded': 17, 'noble_temple': 1}
- dominant_always_gp_only: False
- dominant_always_multifactor: False
**Observations**
- Gp-only best counts: {'self_funded': 19, 'noble_temple': 1} (dominant=False); multifactor counts: {'sovereign': 2, 'self_funded': 17, 'noble_temple': 1} (dominant=False).
- Gp-only scoring often crowns self-funded because share % dominates weak loan friction.
- When seizure risk + appraisal access + political cover are valued, multifactor picks diversify.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: guild-sponsor

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- best_sponsor_counts_gp_only: {'self_funded': 19, 'noble_temple': 1}
- best_sponsor_multifactor_counts: {'sovereign': 2, 'self_funded': 17, 'noble_temple': 1}
- dominant_always_gp_only: False
- dominant_always_multifactor: False
**Observations**
- Gp-only best counts: {'self_funded': 19, 'noble_temple': 1} (dominant=False); multifactor counts: {'sovereign': 2, 'self_funded': 17, 'noble_temple': 1} (dominant=False).
- Observed: naive treasury math makes self-funded dominant; RAW up-front support lacks priced benefits.
- Gp-only scoring often crowns self-funded because share % dominates weak loan friction.
- When seizure risk + appraisal access + political cover are valued, multifactor picks diversify.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?
**Exploits**
- Gp-only players can treat self-funded as always correct unless capital gates are harsh.
**Recommendations**
- Price appraisal access, seizure cover, and capital in gp-equivalent or standing so sponsor choice stays meaningful.

### Agent: haven-magistrate

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- best_sponsor_counts_gp_only: {'self_funded': 19, 'noble_temple': 1}
- best_sponsor_multifactor_counts: {'sovereign': 2, 'self_funded': 17, 'noble_temple': 1}
- dominant_always_gp_only: False
- dominant_always_multifactor: False
**Observations**
- Gp-only best counts: {'self_funded': 19, 'noble_temple': 1} (dominant=False); multifactor counts: {'sovereign': 2, 'self_funded': 17, 'noble_temple': 1} (dominant=False).
- Gp-only scoring often crowns self-funded because share % dominates weak loan friction.
- When seizure risk + appraisal access + political cover are valued, multifactor picks diversify.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: labor-organizer

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- best_sponsor_counts_gp_only: {'self_funded': 19, 'noble_temple': 1}
- best_sponsor_multifactor_counts: {'sovereign': 2, 'self_funded': 17, 'noble_temple': 1}
- dominant_always_gp_only: False
- dominant_always_multifactor: False
**Observations**
- Gp-only best counts: {'self_funded': 19, 'noble_temple': 1} (dominant=False); multifactor counts: {'sovereign': 2, 'self_funded': 17, 'noble_temple': 1} (dominant=False).
- Gp-only scoring often crowns self-funded because share % dominates weak loan friction.
- When seizure risk + appraisal access + political cover are valued, multifactor picks diversify.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: market-auditor

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- best_sponsor_counts_gp_only: {'self_funded': 19, 'noble_temple': 1}
- best_sponsor_multifactor_counts: {'sovereign': 2, 'self_funded': 17, 'noble_temple': 1}
- dominant_always_gp_only: False
- dominant_always_multifactor: False
- auditor_recompute_note: Recomputed all seed settlements in harness; see sim export
**Observations**
- Gp-only best counts: {'self_funded': 19, 'noble_temple': 1} (dominant=False); multifactor counts: {'sovereign': 2, 'self_funded': 17, 'noble_temple': 1} (dominant=False).
- Observed: naive treasury math makes self-funded dominant; RAW up-front support lacks priced benefits.
- Gp-only scoring often crowns self-funded because share % dominates weak loan friction.
- When seizure risk + appraisal access + political cover are valued, multifactor picks diversify.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?
**Exploits**
- Gp-only players can treat self-funded as always correct unless capital gates are harsh.
**Recommendations**
- Price appraisal access, seizure cover, and capital in gp-equivalent or standing so sponsor choice stays meaningful.

### Agent: pleasure-house-operator

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- best_sponsor_counts_gp_only: {'self_funded': 19, 'noble_temple': 1}
- best_sponsor_multifactor_counts: {'sovereign': 2, 'self_funded': 17, 'noble_temple': 1}
- dominant_always_gp_only: False
- dominant_always_multifactor: False
**Observations**
- Gp-only best counts: {'self_funded': 19, 'noble_temple': 1} (dominant=False); multifactor counts: {'sovereign': 2, 'self_funded': 17, 'noble_temple': 1} (dominant=False).
- Gp-only scoring often crowns self-funded because share % dominates weak loan friction.
- When seizure risk + appraisal access + political cover are valued, multifactor picks diversify.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: smuggler

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- best_sponsor_counts_gp_only: {'self_funded': 19, 'noble_temple': 1}
- best_sponsor_multifactor_counts: {'sovereign': 2, 'self_funded': 17, 'noble_temple': 1}
- dominant_always_gp_only: False
- dominant_always_multifactor: False
**Observations**
- Gp-only best counts: {'self_funded': 19, 'noble_temple': 1} (dominant=False); multifactor counts: {'sovereign': 2, 'self_funded': 17, 'noble_temple': 1} (dominant=False).
- Gp-only scoring often crowns self-funded because share % dominates weak loan friction.
- When seizure risk + appraisal access + political cover are valued, multifactor picks diversify.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

## Scenario: HAV-SUBSTANCE

### Agent: anti-trafficking-investigator

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- mean_gross: 2263.1
- seizure_events: 7
- dependence_events: 139
**Observations**
- Quickglass/Redwake/Ghostwine: mean gross 2263.1; seizures=7; dependence events=139.
- Core Systems supplies price_gp, dependence_dc, legality, crash - not market premiums or rehab costs.
- Licensed Quickglass trade profitable but dependence DC 13 catches scouts - Strain on next descent.
- Black-market Redwake seized at quarantine step 1 of Haven order - gross zero, reputation hit.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: artifact-appraiser

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- mean_gross: 2263.1
- seizure_events: 7
- dependence_events: 139
**Observations**
- Quickglass/Redwake/Ghostwine: mean gross 2263.1; seizures=7; dependence events=139.
- Core Systems supplies price_gp, dependence_dc, legality, crash - not market premiums or rehab costs.
- Licensed Quickglass trade profitable but dependence DC 13 catches scouts - Strain on next descent.
- Black-market Redwake seized at quarantine step 1 of Haven order - gross zero, reputation hit.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: brewer-alchemist

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- mean_gross: 2263.1
- seizure_events: 7
- dependence_events: 139
**Observations**
- Quickglass/Redwake/Ghostwine: mean gross 2263.1; seizures=7; dependence events=139.
- Core Systems supplies price_gp, dependence_dc, legality, crash - not market premiums or rehab costs.
- Licensed Quickglass trade profitable but dependence DC 13 catches scouts - Strain on next descent.
- Black-market Redwake seized at quarantine step 1 of Haven order - gross zero, reputation hit.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?
**Recommendations**
- Add Draughtworks rehab Haven Turn cost and licensed vs black-market price bands.

### Agent: expedition-quartermaster

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- mean_gross: 2263.1
- seizure_events: 7
- dependence_events: 139
**Observations**
- Quickglass/Redwake/Ghostwine: mean gross 2263.1; seizures=7; dependence events=139.
- Core Systems supplies price_gp, dependence_dc, legality, crash - not market premiums or rehab costs.
- Substance lots rarely out-earn a rare artifact at equal Load - extraction remains primary.
- Licensed Quickglass trade profitable but dependence DC 13 catches scouts - Strain on next descent.
- Black-market Redwake seized at quarantine step 1 of Haven order - gross zero, reputation hit.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: faction-broker

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- mean_gross: 2263.1
- seizure_events: 7
- dependence_events: 139
- standing_scale_conflict: Loop -5..+5 vs reputation.js Hated/Disliked/Neutral/Liked/Honored
**Observations**
- Quickglass/Redwake/Ghostwine: mean gross 2263.1; seizures=7; dependence events=139.
- Core Systems supplies price_gp, dependence_dc, legality, crash - not market premiums or rehab costs.
- Licensed Quickglass trade profitable but dependence DC 13 catches scouts - Strain on next descent.
- Black-market Redwake seized at quarantine step 1 of Haven order - gross zero, reputation hit.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: goblin-banker

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- mean_gross: 2263.1
- seizure_events: 7
- dependence_events: 139
**Observations**
- Quickglass/Redwake/Ghostwine: mean gross 2263.1; seizures=7; dependence events=139.
- Core Systems supplies price_gp, dependence_dc, legality, crash - not market premiums or rehab costs.
- Licensed Quickglass trade profitable but dependence DC 13 catches scouts - Strain on next descent.
- Black-market Redwake seized at quarantine step 1 of Haven order - gross zero, reputation hit.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: guild-sponsor

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- mean_gross: 2263.1
- seizure_events: 7
- dependence_events: 139
**Observations**
- Quickglass/Redwake/Ghostwine: mean gross 2263.1; seizures=7; dependence events=139.
- Core Systems supplies price_gp, dependence_dc, legality, crash - not market premiums or rehab costs.
- Licensed Quickglass trade profitable but dependence DC 13 catches scouts - Strain on next descent.
- Black-market Redwake seized at quarantine step 1 of Haven order - gross zero, reputation hit.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: haven-magistrate

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- mean_gross: 2263.1
- seizure_events: 7
- dependence_events: 139
**Observations**
- Quickglass/Redwake/Ghostwine: mean gross 2263.1; seizures=7; dependence events=139.
- Core Systems supplies price_gp, dependence_dc, legality, crash - not market premiums or rehab costs.
- Restricted/Military legality should gate quarantine seizure before sale.
- Licensed Quickglass trade profitable but dependence DC 13 catches scouts - Strain on next descent.
- Black-market Redwake seized at quarantine step 1 of Haven order - gross zero, reputation hit.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: labor-organizer

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- mean_gross: 2263.1
- seizure_events: 7
- dependence_events: 139
**Observations**
- Quickglass/Redwake/Ghostwine: mean gross 2263.1; seizures=7; dependence events=139.
- Core Systems supplies price_gp, dependence_dc, legality, crash - not market premiums or rehab costs.
- Licensed Quickglass trade profitable but dependence DC 13 catches scouts - Strain on next descent.
- Black-market Redwake seized at quarantine step 1 of Haven order - gross zero, reputation hit.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: market-auditor

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- mean_gross: 2263.1
- seizure_events: 7
- dependence_events: 139
- auditor_recompute_note: Recomputed all seed settlements in harness; see sim export
**Observations**
- Quickglass/Redwake/Ghostwine: mean gross 2263.1; seizures=7; dependence events=139.
- Core Systems supplies price_gp, dependence_dc, legality, crash - not market premiums or rehab costs.
- Licensed Quickglass trade profitable but dependence DC 13 catches scouts - Strain on next descent.
- Black-market Redwake seized at quarantine step 1 of Haven order - gross zero, reputation hit.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: pleasure-house-operator

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- mean_gross: 2263.1
- seizure_events: 7
- dependence_events: 139
**Observations**
- Quickglass/Redwake/Ghostwine: mean gross 2263.1; seizures=7; dependence events=139.
- Core Systems supplies price_gp, dependence_dc, legality, crash - not market premiums or rehab costs.
- Licensed Quickglass trade profitable but dependence DC 13 catches scouts - Strain on next descent.
- Black-market Redwake seized at quarantine step 1 of Haven order - gross zero, reputation hit.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: smuggler

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- mean_gross: 2263.1
- seizure_events: 7
- dependence_events: 139
**Observations**
- Quickglass/Redwake/Ghostwine: mean gross 2263.1; seizures=7; dependence events=139.
- Core Systems supplies price_gp, dependence_dc, legality, crash - not market premiums or rehab costs.
- Licensed Quickglass trade profitable but dependence DC 13 catches scouts - Strain on next descent.
- Black-market Redwake seized at quarantine step 1 of Haven order - gross zero, reputation hit.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

## Scenario: HAV-TRAFFICKING

### Agent: anti-trafficking-investigator

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- prosecution_rate: 0.15
- consequence_free_rate: 0.3
**Observations**
- Trafficking claims: prosecution 15%; consequence-free illegal commerce 30% when evidence fails.
- Played as victims/resistance/law/reputation - not a decorative price list (orchestrator rule).
- Inspection always precedes claims per Haven resolution order - trafficking cannot skip quarantine.
- Illegal sale with failed evidence sometimes yields gp - identified exploit: evidence gap.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?
**Exploits**
- Evidence-failure path can still yield ~70% sale proxy - trafficking not fully consequence-closed.
**Recommendations**
- Tie quarantine inspection to automatic evidence clock; illegal_sale claims require public hearing.

### Agent: artifact-appraiser

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- prosecution_rate: 0.15
- consequence_free_rate: 0.3
**Observations**
- Trafficking claims: prosecution 15%; consequence-free illegal commerce 30% when evidence fails.
- Played as victims/resistance/law/reputation - not a decorative price list (orchestrator rule).
- Inspection always precedes claims per Haven resolution order - trafficking cannot skip quarantine.
- Illegal sale with failed evidence sometimes yields gp - identified exploit: evidence gap.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: brewer-alchemist

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- prosecution_rate: 0.15
- consequence_free_rate: 0.3
**Observations**
- Trafficking claims: prosecution 15%; consequence-free illegal commerce 30% when evidence fails.
- Played as victims/resistance/law/reputation - not a decorative price list (orchestrator rule).
- Inspection always precedes claims per Haven resolution order - trafficking cannot skip quarantine.
- Illegal sale with failed evidence sometimes yields gp - identified exploit: evidence gap.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: expedition-quartermaster

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- prosecution_rate: 0.15
- consequence_free_rate: 0.3
**Observations**
- Trafficking claims: prosecution 15%; consequence-free illegal commerce 30% when evidence fails.
- Played as victims/resistance/law/reputation - not a decorative price list (orchestrator rule).
- Inspection always precedes claims per Haven resolution order - trafficking cannot skip quarantine.
- Illegal sale with failed evidence sometimes yields gp - identified exploit: evidence gap.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: faction-broker

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- prosecution_rate: 0.15
- consequence_free_rate: 0.3
- standing_scale_conflict: Loop -5..+5 vs reputation.js Hated/Disliked/Neutral/Liked/Honored
**Observations**
- Trafficking claims: prosecution 15%; consequence-free illegal commerce 30% when evidence fails.
- Played as victims/resistance/law/reputation - not a decorative price list (orchestrator rule).
- Inspection always precedes claims per Haven resolution order - trafficking cannot skip quarantine.
- Illegal sale with failed evidence sometimes yields gp - identified exploit: evidence gap.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: goblin-banker

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- prosecution_rate: 0.15
- consequence_free_rate: 0.3
**Observations**
- Trafficking claims: prosecution 15%; consequence-free illegal commerce 30% when evidence fails.
- Played as victims/resistance/law/reputation - not a decorative price list (orchestrator rule).
- Inspection always precedes claims per Haven resolution order - trafficking cannot skip quarantine.
- Illegal sale with failed evidence sometimes yields gp - identified exploit: evidence gap.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: guild-sponsor

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- prosecution_rate: 0.15
- consequence_free_rate: 0.3
**Observations**
- Trafficking claims: prosecution 15%; consequence-free illegal commerce 30% when evidence fails.
- Played as victims/resistance/law/reputation - not a decorative price list (orchestrator rule).
- Inspection always precedes claims per Haven resolution order - trafficking cannot skip quarantine.
- Illegal sale with failed evidence sometimes yields gp - identified exploit: evidence gap.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: haven-magistrate

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- prosecution_rate: 0.15
- consequence_free_rate: 0.3
**Observations**
- Trafficking claims: prosecution 15%; consequence-free illegal commerce 30% when evidence fails.
- Played as victims/resistance/law/reputation - not a decorative price list (orchestrator rule).
- Haven order step 1 quarantine correctly blocks silent Chain Market dumps.
- Inspection always precedes claims per Haven resolution order - trafficking cannot skip quarantine.
- Illegal sale with failed evidence sometimes yields gp - identified exploit: evidence gap.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: labor-organizer

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- prosecution_rate: 0.15
- consequence_free_rate: 0.3
**Observations**
- Trafficking claims: prosecution 15%; consequence-free illegal commerce 30% when evidence fails.
- Played as victims/resistance/law/reputation - not a decorative price list (orchestrator rule).
- Inspection always precedes claims per Haven resolution order - trafficking cannot skip quarantine.
- Illegal sale with failed evidence sometimes yields gp - identified exploit: evidence gap.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: market-auditor

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- prosecution_rate: 0.15
- consequence_free_rate: 0.3
- auditor_recompute_note: Recomputed all seed settlements in harness; see sim export
**Observations**
- Trafficking claims: prosecution 15%; consequence-free illegal commerce 30% when evidence fails.
- Played as victims/resistance/law/reputation - not a decorative price list (orchestrator rule).
- Inspection always precedes claims per Haven resolution order - trafficking cannot skip quarantine.
- Illegal sale with failed evidence sometimes yields gp - identified exploit: evidence gap.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: pleasure-house-operator

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- prosecution_rate: 0.15
- consequence_free_rate: 0.3
**Observations**
- Trafficking claims: prosecution 15%; consequence-free illegal commerce 30% when evidence fails.
- Played as victims/resistance/law/reputation - not a decorative price list (orchestrator rule).
- Kept consensual adult work out of trafficking scenario - institutional boundary held.
- Inspection always precedes claims per Haven resolution order - trafficking cannot skip quarantine.
- Illegal sale with failed evidence sometimes yields gp - identified exploit: evidence gap.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

### Agent: smuggler

**Metrics**
- seeds_run: 20
- narratives_run: 5
- source_gameplay_loop: pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)
- source_haven: src/data/haven.json
- prosecution_rate: 0.15
- consequence_free_rate: 0.3
**Observations**
- Trafficking claims: prosecution 15%; consequence-free illegal commerce 30% when evidence fails.
- Played as victims/resistance/law/reputation - not a decorative price list (orchestrator rule).
- Inspection always precedes claims per Haven resolution order - trafficking cannot skip quarantine.
- Illegal sale with failed evidence sometimes yields gp - identified exploit: evidence gap.
**Rules questions**
- GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?

## Repeated rules questions

- (120) GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract.
- (120) Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption.
- (120) reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?
- (1) Is there a published buyer table for 'best current buyer' on critical success?
- (1) Quarantine can force urgency=forced (0.75); need explicit clock tying inspection delay to urgency.
- (1) What are Makers' Quarter production costs, spoilage clocks, and license fees by brew tier?
- (1) Publish assay DC by adulteration %, remint fee, and collateral rules for Iron Ledger Houses.
- (1) Publish fair wage, max advance interest, strike resolution, and emancipation buyout formula.
- (1) Many crafting materials lack gp baseValue - market shock math needs explicit Haven commodity prices.
- (1) Publish Low Lantern patronage, information brokerage, and worker-protection license rules.
- (1) How much standing does political cover grant, and is it inside the +/-2 per-scene cap?

## Repeated exploit findings

- (3) Gp-only players can treat self-funded as always correct unless capital gates are harsh.
- (1) If Directors skip provenance filing, undocumented 0.5 multiplier never applies - infinite soft profit vs RAW.
- (1) Without remint fees, players can treat shaved coin at face indefinitely - infinite soft profit.
- (1) If catch rate house-ruled to ~0 and standing hits ignored, smuggling can dominate legal guild path.
- (1) Evidence-failure path can still yield ~70% sale proxy - trafficking not fully consequence-closed.

## Repeated recommendations

- (3) Price appraisal access, seizure cover, and capital in gp-equivalent or standing so sponsor choice stays meaningful.
- (1) Publish wage/repair line items so Quartermaster can refuse incomplete settlement sheets.
- (1) Record economic shocks on Cycle Record (Loop section 20) for pack 04 continuity.
- (1) Publish Underways seizure table + bribery as criminal procedure with standing costs.
- (1) Add Draughtworks rehab Haven Turn cost and licensed vs black-market price bands.
- (1) Tie quarantine inspection to automatic evidence clock; illegal_sale claims require public hearing.

