# Herbalism Director internal recipe cards

**Draft awaiting exact GPT review.** All 45 formulas: 29 public, three restricted and 13 Director-only. Keep this file internal.

Use the [shared procedures](../mechanics/HERBALISM_RECIPE_PLAYTEST.md) with every card. Original fields remain in the JSON and source evidence. Names do not grant equipment grades or additional powers. Prices below refer to an entire Standard batch and need an actual buyer/supplier quote.

## recipe-200 — Refined Frost Antidote

**Source:** public; Herbalism level 4; tier 2; Common; DC 10; 2 active hours; 5 doses. Standard batch reference 61 gp.

**Preserved effect:** Ends the poisoned condition and grants advantage on saves against poison for 10 minutes.

**Operational effect:** End every present removable Poisoned application, without deleting its independent underlying cause; future exposure may reapply it. Gain advantage on saves against poison for 10 elapsed minutes. No added numeric bonus, poison immunity, resistance, disease or intoxication cure.

**Administration:** Action, one available hand, drink or feed a compatible willing or Incapacitated recipient within 5 feet. Spend one actual dose at legal start. No benefit until completion; interruption does not refund it.

**Work:** Herbalist's Table; Herbalism kit, Mortar and pestle, Drying rack. Mode field; field flag true; up to 0 assistants; formula required false.

**Exact ingredients:** 4 × Purified water (component tier 2; 0.5 lb/unit; 8 gp/unit; solvent; consumed); 1 × sparkling petal (component tier 1; 0.36 lb/unit; 10 gp/unit; material; consumed).

**Packaging:** no source vessels. Reserve 5 actual Glass vials for Standard output; 6 for Exceptional yield; 7 for full Masterwork yield. Each filled vial is 0.2 lb and one dose. At maximum yield with any eligible catalyst returned, reserve 0 lb additional clean carrier water. Owned intact spent vials may be reused; new ordinary Glass vials have a 1-gp reference price. All chosen-output packaging and carrier must be present before the check.

**Flawed:** {"mode": "half-batch-quantity", "quantity": 2, "effectChange": null}. Exceptional/Masterwork choose finite yield or Standard quantity with every container at max/current HP 2, never both. No effect potency or extra cures.

**Provenance:** current effect and original ingredient identities are retained. Legacy fields remain in source/JSON and are inactive. No source deletion.

## recipe-201 — Superior Storm Balm of Sparkling Petal

**Source:** public; Herbalism level 5; tier 3; Common; DC 8; 4 active hours; 4 doses. Standard batch reference 57 gp.

**Preserved effect:** Applied over 1 minute, restores 1d6+2 hit points and treats one wound, burn, or infection appropriate to its ingredients.

**Operational effect:** After one uninterrupted active minute, attempt 1d6+2 ordinary magical nonspell HP healing under actual caps and blockers. After healing and its condition endpoints, choose at most one present local wound, burn, infection or Bleeding source appropriate to topical treatment. A Bleeding source with an existing Medicine-based removal DC permits one immediate WIS (Medicine) check against that DC using this dose as dressing, with no extra healer-kit charge. Do not attempt this if this dose already resolved a healing-triggered removal/treatment attempt for that record. Otherwise it supplies only one expressly required topical dressing/cleaning step in the source procedure; every other time, check, Supply, kit, medicine, rest and cure requirement remains. No defined interaction means no extra condition removal.

**Administration:** 1 uninterrupted active minute(s), requiring 10 consecutive regular-turn Actions in initiative and the full elapsed interval; keep touch and one hand available. Spend one actual dose at legal start. No benefit until completion; interruption does not refund it.

**Work:** Herbalist's Table; Herbalism kit, Mortar and pestle, Drying rack. Mode expedition; field flag true; up to 0 assistants; formula required true.

**Exact ingredients:** 1 × Dried flowers (component tier 3; 0.1 lb/unit; 25 gp/unit; substrate; consumed); 1 × sparkling petal (component tier 1; 0.36 lb/unit; 10 gp/unit; material; consumed).

**Packaging:** no source vessels. Reserve 4 actual Glass vials for Standard output; 5 for Exceptional yield; 6 for full Masterwork yield. Each filled vial is 0.2 lb and one dose. At maximum yield with any eligible catalyst returned, reserve 0.14 lb additional clean carrier water. Owned intact spent vials may be reused; new ordinary Glass vials have a 1-gp reference price. All chosen-output packaging and carrier must be present before the check.

**Flawed:** {"mode": "half-batch-quantity", "quantity": 2, "effectChange": null}. Exceptional/Masterwork choose finite yield or Standard quantity with every container at max/current HP 2, never both. No effect potency or extra cures.

**Provenance:** current effect and original ingredient identities are retained. Legacy fields remain in source/JSON and are inactive. No source deletion.

## recipe-202 — Refined Vital Compress

**Source:** public; Herbalism level 4; tier 2; Common; DC 9; 1 active hours; 4 doses. Standard batch reference 72 gp.

**Preserved effect:** Applied over 1 minute, restores 1d6+2 hit points and treats one wound, burn, or infection appropriate to its ingredients.

**Operational effect:** After one uninterrupted active minute, attempt 1d6+2 ordinary magical nonspell HP healing under actual caps and blockers. After healing and its condition endpoints, choose at most one present local wound, burn, infection or Bleeding source appropriate to topical treatment. A Bleeding source with an existing Medicine-based removal DC permits one immediate WIS (Medicine) check against that DC using this dose as dressing, with no extra healer-kit charge. Do not attempt this if this dose already resolved a healing-triggered removal/treatment attempt for that record. Otherwise it supplies only one expressly required topical dressing/cleaning step in the source procedure; every other time, check, Supply, kit, medicine, rest and cure requirement remains. No defined interaction means no extra condition removal.

**Administration:** 1 uninterrupted active minute(s), requiring 10 consecutive regular-turn Actions in initiative and the full elapsed interval; keep touch and one hand available. Spend one actual dose at legal start. No benefit until completion; interruption does not refund it.

**Work:** Herbalist's Table; Herbalism kit, Mortar and pestle, Drying rack. Mode field; field flag true; up to 0 assistants; formula required false.

**Exact ingredients:** 1 × Healing roots (component tier 2; 0.1 lb/unit; 8 gp/unit; substrate; consumed); 1 × Mortar and pestle (component tier 2; 1.0 lb/unit; 24 gp/unit; tool; returned); 4 × Beeswax (component tier 2; 0.1 lb/unit; 8 gp/unit; binder; consumed); 1 × living root (component tier 1; 0.29 lb/unit; 12 gp/unit; material; consumed).

**Packaging:** no source vessels. Reserve 4 actual Glass vials for Standard output; 5 for Exceptional yield; 6 for full Masterwork yield. Each filled vial is 0.2 lb and one dose. At maximum yield with any eligible catalyst returned, reserve 0 lb additional clean carrier water. Owned intact spent vials may be reused; new ordinary Glass vials have a 1-gp reference price. All chosen-output packaging and carrier must be present before the check.

**Flawed:** {"mode": "half-batch-quantity", "quantity": 2, "effectChange": null}. Exceptional/Masterwork choose finite yield or Standard quantity with every container at max/current HP 2, never both. No effect potency or extra cures.

**Provenance:** current effect and original ingredient identities are retained. Legacy fields remain in source/JSON and are inactive. No source deletion.

## recipe-203 — Refined Ember Healing Salve

**Source:** public; Herbalism level 3; tier 2; Common; DC 12; 2 active hours; 1 doses. Standard batch reference 49 gp.

**Preserved effect:** Applied over 1 minute, restores 1d6+2 hit points and treats one wound, burn, or infection appropriate to its ingredients.

**Operational effect:** After one uninterrupted active minute, attempt 1d6+2 ordinary magical nonspell HP healing under actual caps and blockers. After healing and its condition endpoints, choose at most one present local wound, burn, infection or Bleeding source appropriate to topical treatment. A Bleeding source with an existing Medicine-based removal DC permits one immediate WIS (Medicine) check against that DC using this dose as dressing, with no extra healer-kit charge. Do not attempt this if this dose already resolved a healing-triggered removal/treatment attempt for that record. Otherwise it supplies only one expressly required topical dressing/cleaning step in the source procedure; every other time, check, Supply, kit, medicine, rest and cure requirement remains. No defined interaction means no extra condition removal.

**Administration:** 1 uninterrupted active minute(s), requiring 10 consecutive regular-turn Actions in initiative and the full elapsed interval; keep touch and one hand available. Spend one actual dose at legal start. No benefit until completion; interruption does not refund it.

**Work:** Herbalist's Table; Herbalism kit, Mortar and pestle, Drying rack. Mode field; field flag true; up to 0 assistants; formula required false.

**Exact ingredients:** 1 × Honey (component tier 2; 0.1 lb/unit; 8 gp/unit; seasoning; consumed); 2 × Crushed leaves (component tier 2; 0.1 lb/unit; 8 gp/unit; ingredient; consumed); 1 × sparkling petal (component tier 1; 0.36 lb/unit; 10 gp/unit; material; consumed).

**Packaging:** no source vessels. Reserve 1 actual Glass vials for Standard output; 1 for Exceptional yield; 1 for full Masterwork yield. Each filled vial is 0.2 lb and one dose. At maximum yield with any eligible catalyst returned, reserve 0 lb additional clean carrier water. Owned intact spent vials may be reused; new ordinary Glass vials have a 1-gp reference price. All chosen-output packaging and carrier must be present before the check.

**Flawed:** {"mode": "treat-as-Failed", "quantity": 0, "recovery": "framework 25 percent non-catalyst inputs"}. Exceptional/Masterwork choose finite yield or Standard quantity with every container at max/current HP 2, never both. No effect potency or extra cures.

**Provenance:** current effect and original ingredient identities are retained. Legacy fields remain in source/JSON and are inactive. No source deletion.

## recipe-204 — Refined Venom Powder

**Source:** public; Herbalism level 3; tier 2; Common; DC 10; 4 active hours; 5 doses. Standard batch reference 79 gp.

**Preserved effect:** Grants +1 to saves and checks related to poison hazards for 10 minutes.

**Operational effect:** Gain +1 on the recipient's own qualifying checks and saves against Poison hazards for 10 elapsed minutes. Saves against actual poison or Poisoned effects; checks directly identifying, avoiding, safely handling or disabling an actual poison hazard. No attack/damage bonus, automatic resistance, extra save or resource recovery.

**Administration:** Action, one available hand, drink or feed a compatible willing or Incapacitated recipient within 5 feet. Spend one actual dose at legal start. No benefit until completion; interruption does not refund it.

**Work:** Herbalist's Table; Herbalism kit, Mortar and pestle, Drying rack. Mode expedition; field flag true; up to 0 assistants; formula required false.

**Exact ingredients:** 5 × Natural oils (component tier 2; 0.5 lb/unit; 8 gp/unit; solvent; consumed); 1 × Poisonous meat (component tier 1; 0.38 lb/unit; 14 gp/unit; catalyst; consumed).

**Packaging:** no source vessels. Reserve 5 actual Glass vials for Standard output; 6 for Exceptional yield; 7 for full Masterwork yield. Each filled vial is 0.2 lb and one dose. At maximum yield with any eligible catalyst returned, reserve 0 lb additional clean carrier water. Owned intact spent vials may be reused; new ordinary Glass vials have a 1-gp reference price. All chosen-output packaging and carrier must be present before the check.

**Flawed:** {"mode": "half-batch-quantity", "quantity": 2, "effectChange": null}. Exceptional/Masterwork choose finite yield or Standard quantity with every container at max/current HP 2, never both. No effect potency or extra cures.

**Provenance:** current effect and original ingredient identities are retained. Legacy fields remain in source/JSON and are inactive. No source deletion.

## recipe-205 — Refined Ember Compress

**Source:** public; Herbalism level 3; tier 2; Common; DC 12; 1 active hours; 4 doses. Standard batch reference 72 gp.

**Preserved effect:** Applied over 1 minute, restores 1d6+2 hit points and treats one wound, burn, or infection appropriate to its ingredients.

**Operational effect:** After one uninterrupted active minute, attempt 1d6+2 ordinary magical nonspell HP healing under actual caps and blockers. After healing and its condition endpoints, choose at most one present local wound, burn, infection or Bleeding source appropriate to topical treatment. A Bleeding source with an existing Medicine-based removal DC permits one immediate WIS (Medicine) check against that DC using this dose as dressing, with no extra healer-kit charge. Do not attempt this if this dose already resolved a healing-triggered removal/treatment attempt for that record. Otherwise it supplies only one expressly required topical dressing/cleaning step in the source procedure; every other time, check, Supply, kit, medicine, rest and cure requirement remains. No defined interaction means no extra condition removal.

**Administration:** 1 uninterrupted active minute(s), requiring 10 consecutive regular-turn Actions in initiative and the full elapsed interval; keep touch and one hand available. Spend one actual dose at legal start. No benefit until completion; interruption does not refund it.

**Work:** Herbalist's Table; Herbalism kit, Mortar and pestle, Drying rack. Mode field; field flag true; up to 0 assistants; formula required false.

**Exact ingredients:** 5 × Honey (component tier 2; 0.1 lb/unit; 8 gp/unit; seasoning; consumed); 1 × living root (component tier 1; 0.29 lb/unit; 12 gp/unit; material; consumed).

**Packaging:** no source vessels. Reserve 4 actual Glass vials for Standard output; 5 for Exceptional yield; 6 for full Masterwork yield. Each filled vial is 0.2 lb and one dose. At maximum yield with any eligible catalyst returned, reserve 0 lb additional clean carrier water. Owned intact spent vials may be reused; new ordinary Glass vials have a 1-gp reference price. All chosen-output packaging and carrier must be present before the check.

**Flawed:** {"mode": "half-batch-quantity", "quantity": 2, "effectChange": null}. Exceptional/Masterwork choose finite yield or Standard quantity with every container at max/current HP 2, never both. No effect potency or extra cures.

**Provenance:** current effect and original ingredient identities are retained. Legacy fields remain in source/JSON and are inactive. No source deletion.

## recipe-206 — Refined Venom Tonic

**Source:** public; Herbalism level 4; tier 2; Common; DC 12; 4 active hours; 5 doses. Standard batch reference 156 gp.

**Preserved effect:** Grants +1 to saves and checks related to poison hazards for 10 minutes.

**Operational effect:** Gain +1 on the recipient's own qualifying checks and saves against Poison hazards for 10 elapsed minutes. Saves against actual poison or Poisoned effects; checks directly identifying, avoiding, safely handling or disabling an actual poison hazard. No attack/damage bonus, automatic resistance, extra save or resource recovery.

**Administration:** Action, one available hand, drink or feed a compatible willing or Incapacitated recipient within 5 feet. Spend one actual dose at legal start. No benefit until completion; interruption does not refund it.

**Work:** Herbalist's Table; Herbalism kit, Mortar and pestle, Drying rack. Mode expedition; field flag true; up to 0 assistants; formula required false.

**Exact ingredients:** 3 × Purified water (component tier 2; 0.5 lb/unit; 8 gp/unit; solvent; consumed); 5 × Crushed leaves (component tier 2; 0.1 lb/unit; 8 gp/unit; ingredient; consumed); 4 × Healing roots (component tier 2; 0.1 lb/unit; 8 gp/unit; substrate; consumed); 1 × Poisonous meat (component tier 1; 0.38 lb/unit; 14 gp/unit; catalyst; consumed).

**Packaging:** no source vessels. Reserve 5 actual Glass vials for Standard output; 6 for Exceptional yield; 7 for full Masterwork yield. Each filled vial is 0.2 lb and one dose. At maximum yield with any eligible catalyst returned, reserve 0 lb additional clean carrier water. Owned intact spent vials may be reused; new ordinary Glass vials have a 1-gp reference price. All chosen-output packaging and carrier must be present before the check.

**Flawed:** {"mode": "half-batch-quantity", "quantity": 2, "effectChange": null}. Exceptional/Masterwork choose finite yield or Standard quantity with every container at max/current HP 2, never both. No effect potency or extra cures.

**Provenance:** current effect and original ingredient identities are retained. Legacy fields remain in source/JSON and are inactive. No source deletion.

## recipe-207 — Superior Caustic Tea of Caustic Goo

**Source:** public; Herbalism level 5; tier 3; Common; DC 12; 4 active hours; 2 doses. Standard batch reference 325 gp.

**Preserved effect:** Grants +1 to saves and checks related to acid hazards for 10 minutes.

**Operational effect:** Gain +1 on the recipient's own qualifying checks and saves against Acid hazards for 10 elapsed minutes. Saves against actual acid-damage or corrosive hazards; checks directly handling, avoiding or disabling such a hazard. No attack/damage bonus, automatic resistance, extra save or resource recovery.

**Administration:** Action, one available hand, drink or feed a compatible willing or Incapacitated recipient within 5 feet. Spend one actual dose at legal start. No benefit until completion; interruption does not refund it.

**Work:** Herbalist's Table; Herbalism kit, Mortar and pestle, Drying rack. Mode expedition; field flag true; up to 0 assistants; formula required true.

**Exact ingredients:** 5 × Beeswax (component tier 3; 0.1 lb/unit; 25 gp/unit; binder; consumed); 4 × Medicinal herbs (component tier 3; 0.1 lb/unit; 25 gp/unit; substrate; consumed); 1 × caustic goo (component tier 1; 0.99 lb/unit; 8 gp/unit; material; consumed).

**Packaging:** no source vessels. Reserve 2 actual Glass vials for Standard output; 2 for Exceptional yield; 3 for full Masterwork yield. Each filled vial is 0.2 lb and one dose. At maximum yield with any eligible catalyst returned, reserve 0 lb additional clean carrier water. Owned intact spent vials may be reused; new ordinary Glass vials have a 1-gp reference price. All chosen-output packaging and carrier must be present before the check.

**Flawed:** {"mode": "half-batch-quantity", "quantity": 1, "effectChange": null}. Exceptional/Masterwork choose finite yield or Standard quantity with every container at max/current HP 2, never both. No effect potency or extra cures.

**Provenance:** current effect and original ingredient identities are retained. Legacy fields remain in source/JSON and are inactive. No source deletion.

## recipe-208 — Refined Caustic Healing Salve

**Source:** public; Herbalism level 4; tier 2; Common; DC 9; 4 active hours; 5 doses. Standard batch reference 51 gp.

**Preserved effect:** Applied over 1 minute, restores 1d6+2 hit points and treats one wound, burn, or infection appropriate to its ingredients.

**Operational effect:** After one uninterrupted active minute, attempt 1d6+2 ordinary magical nonspell HP healing under actual caps and blockers. After healing and its condition endpoints, choose at most one present local wound, burn, infection or Bleeding source appropriate to topical treatment. A Bleeding source with an existing Medicine-based removal DC permits one immediate WIS (Medicine) check against that DC using this dose as dressing, with no extra healer-kit charge. Do not attempt this if this dose already resolved a healing-triggered removal/treatment attempt for that record. Otherwise it supplies only one expressly required topical dressing/cleaning step in the source procedure; every other time, check, Supply, kit, medicine, rest and cure requirement remains. No defined interaction means no extra condition removal.

**Administration:** 1 uninterrupted active minute(s), requiring 10 consecutive regular-turn Actions in initiative and the full elapsed interval; keep touch and one hand available. Spend one actual dose at legal start. No benefit until completion; interruption does not refund it.

**Work:** Herbalist's Table; Herbalism kit, Mortar and pestle, Drying rack. Mode expedition; field flag true; up to 0 assistants; formula required false.

**Exact ingredients:** 3 × Beeswax (component tier 2; 0.1 lb/unit; 8 gp/unit; binder; consumed); 1 × caustic goo (component tier 1; 0.99 lb/unit; 8 gp/unit; material; consumed).

**Packaging:** no source vessels. Reserve 5 actual Glass vials for Standard output; 6 for Exceptional yield; 7 for full Masterwork yield. Each filled vial is 0.2 lb and one dose. At maximum yield with any eligible catalyst returned, reserve 0 lb additional clean carrier water. Owned intact spent vials may be reused; new ordinary Glass vials have a 1-gp reference price. All chosen-output packaging and carrier must be present before the check.

**Flawed:** {"mode": "half-batch-quantity", "quantity": 2, "effectChange": null}. Exceptional/Masterwork choose finite yield or Standard quantity with every container at max/current HP 2, never both. No effect potency or extra cures.

**Provenance:** current effect and original ingredient identities are retained. Legacy fields remain in source/JSON and are inactive. No source deletion.

## recipe-209 — Superior Grave Tonic of Fiendish Ichor

**Source:** public; Herbalism level 5; tier 3; Common; DC 8; 1 active hours; 2 doses. Standard batch reference 255 gp.

**Preserved effect:** Grants +1 to saves and checks related to unholy hazards for 10 minutes.

**Operational effect:** Gain +1 on the recipient's own qualifying checks and saves against Unholy hazards for 10 elapsed minutes. Only an explicitly mechanically labeled Unholy hazard; never inferred from species, morality, religion, appearance or origin. No attack/damage bonus, automatic resistance, extra save or resource recovery.

**Administration:** Action, one available hand, drink or feed a compatible willing or Incapacitated recipient within 5 feet. Spend one actual dose at legal start. No benefit until completion; interruption does not refund it.

**Work:** Herbalist's Table; Herbalism kit, Mortar and pestle, Drying rack. Mode field; field flag true; up to 0 assistants; formula required true.

**Exact ingredients:** 4 × Crushed leaves (component tier 3; 0.1 lb/unit; 25 gp/unit; ingredient; consumed); 3 × Medicinal herbs (component tier 3; 0.1 lb/unit; 25 gp/unit; substrate; consumed); 1 × fiendish ichor (component tier 1; 0.83 lb/unit; 12 gp/unit; catalyst; consumed).

**Packaging:** no source vessels. Reserve 2 actual Glass vials for Standard output; 2 for Exceptional yield; 3 for full Masterwork yield. Each filled vial is 0.2 lb and one dose. At maximum yield with any eligible catalyst returned, reserve 0 lb additional clean carrier water. Owned intact spent vials may be reused; new ordinary Glass vials have a 1-gp reference price. All chosen-output packaging and carrier must be present before the check.

**Flawed:** {"mode": "half-batch-quantity", "quantity": 1, "effectChange": null}. Exceptional/Masterwork choose finite yield or Standard quantity with every container at max/current HP 2, never both. No effect potency or extra cures.

**Provenance:** current effect and original ingredient identities are retained. Legacy fields remain in source/JSON and are inactive. No source deletion.

## recipe-210 — Refined Stone Remedy

**Source:** public; Herbalism level 3; tier 2; Common; DC 9; 8 active hours; 3 doses. Standard batch reference 884 gp.

**Preserved effect:** Grants +1 to saves and checks related to earth hazards for 10 minutes.

**Operational effect:** Gain +1 on the recipient's own qualifying checks and saves against Earth hazards for 10 elapsed minutes. Rockfall, cave-in, burial, unstable stone or ground, crushing geological movement or another explicitly physical earth/stone hazard; not every event on stone or earth. No attack/damage bonus, automatic resistance, extra save or resource recovery.

**Administration:** Action, one available hand, drink or feed a compatible willing or Incapacitated recipient within 5 feet. Spend one actual dose at legal start. No benefit until completion; interruption does not refund it.

**Work:** Herbalist's Table; Herbalism kit, Mortar and pestle, Drying rack. Mode expedition; field flag true; up to 0 assistants; formula required false.

**Exact ingredients:** 5 × Honey (component tier 2; 0.1 lb/unit; 8 gp/unit; seasoning; consumed); 1 × Healing roots (component tier 2; 0.1 lb/unit; 8 gp/unit; substrate; consumed); 2 × Crushed leaves (component tier 2; 0.1 lb/unit; 8 gp/unit; ingredient; consumed); 1 × shamanic bloodstone (component tier 5; 0.14 lb/unit; 582 gp/unit; catalyst; consumed).

**Packaging:** no source vessels. Reserve 3 actual Glass vials for Standard output; 3 for Exceptional yield; 4 for full Masterwork yield. Each filled vial is 0.2 lb and one dose. At maximum yield with any eligible catalyst returned, reserve 0 lb additional clean carrier water. Owned intact spent vials may be reused; new ordinary Glass vials have a 1-gp reference price. All chosen-output packaging and carrier must be present before the check.

**Flawed:** {"mode": "half-batch-quantity", "quantity": 1, "effectChange": null}. Exceptional/Masterwork choose finite yield or Standard quantity with every container at max/current HP 2, never both. No effect potency or extra cures.

**Provenance:** current effect and original ingredient identities are retained. Legacy fields remain in source/JSON and are inactive. No source deletion.

## recipe-211 — Field Tide Tea

**Source:** public; Herbalism level 1; tier 1; Common; DC 10; 8 active hours; 3 doses. Standard batch reference 37 gp.

**Preserved effect:** Grants +1 to saves and checks related to water hazards for 10 minutes.

**Operational effect:** Gain +1 on the recipient's own qualifying checks and saves against Water hazards for 10 elapsed minutes. Currents, flooding, drowning, undertow, hazardous immersion or another actual water hazard. No attack/damage bonus, automatic resistance, extra save or resource recovery.

**Administration:** Action, one available hand, drink or feed a compatible willing or Incapacitated recipient within 5 feet. Spend one actual dose at legal start. No benefit until completion; interruption does not refund it.

**Work:** Herbalist's Table; Herbalism kit, Mortar and pestle, Drying rack. Mode expedition; field flag true; up to 0 assistants; formula required false.

**Exact ingredients:** 3 × Natural oils (component tier 1; 0.5 lb/unit; 2 gp/unit; solvent; consumed); 1 × sparkling petal (component tier 1; 0.36 lb/unit; 10 gp/unit; material; consumed).

**Packaging:** no source vessels. Reserve 3 actual Glass vials for Standard output; 3 for Exceptional yield; 4 for full Masterwork yield. Each filled vial is 0.2 lb and one dose. At maximum yield with any eligible catalyst returned, reserve 0 lb additional clean carrier water. Owned intact spent vials may be reused; new ordinary Glass vials have a 1-gp reference price. All chosen-output packaging and carrier must be present before the check.

**Flawed:** {"mode": "half-batch-quantity", "quantity": 1, "effectChange": null}. Exceptional/Masterwork choose finite yield or Standard quantity with every container at max/current HP 2, never both. No effect potency or extra cures.

**Provenance:** current effect and original ingredient identities are retained. Legacy fields remain in source/JSON and are inactive. No source deletion.

## recipe-212 — Refined Gale Healing Salve

**Source:** public; Herbalism level 4; tier 2; Common; DC 11; 2 active hours; 4 doses. Standard batch reference 63 gp.

**Preserved effect:** Applied over 1 minute, restores 1d6+2 hit points and treats one wound, burn, or infection appropriate to its ingredients.

**Operational effect:** After one uninterrupted active minute, attempt 1d6+2 ordinary magical nonspell HP healing under actual caps and blockers. After healing and its condition endpoints, choose at most one present local wound, burn, infection or Bleeding source appropriate to topical treatment. A Bleeding source with an existing Medicine-based removal DC permits one immediate WIS (Medicine) check against that DC using this dose as dressing, with no extra healer-kit charge. Do not attempt this if this dose already resolved a healing-triggered removal/treatment attempt for that record. Otherwise it supplies only one expressly required topical dressing/cleaning step in the source procedure; every other time, check, Supply, kit, medicine, rest and cure requirement remains. No defined interaction means no extra condition removal.

**Administration:** 1 uninterrupted active minute(s), requiring 10 consecutive regular-turn Actions in initiative and the full elapsed interval; keep touch and one hand available. Spend one actual dose at legal start. No benefit until completion; interruption does not refund it.

**Work:** Herbalist's Table; Herbalism kit, Mortar and pestle, Drying rack. Mode field; field flag true; up to 0 assistants; formula required false.

**Exact ingredients:** 3 × Purified water (component tier 2; 0.5 lb/unit; 8 gp/unit; solvent; consumed); 1 × Beeswax (component tier 2; 0.1 lb/unit; 8 gp/unit; binder; consumed); 1 × living root (component tier 1; 0.29 lb/unit; 12 gp/unit; material; consumed).

**Packaging:** no source vessels. Reserve 4 actual Glass vials for Standard output; 5 for Exceptional yield; 6 for full Masterwork yield. Each filled vial is 0.2 lb and one dose. At maximum yield with any eligible catalyst returned, reserve 0 lb additional clean carrier water. Owned intact spent vials may be reused; new ordinary Glass vials have a 1-gp reference price. All chosen-output packaging and carrier must be present before the check.

**Flawed:** {"mode": "half-batch-quantity", "quantity": 2, "effectChange": null}. Exceptional/Masterwork choose finite yield or Standard quantity with every container at max/current HP 2, never both. No effect potency or extra cures.

**Provenance:** current effect and original ingredient identities are retained. Legacy fields remain in source/JSON and are inactive. No source deletion.

## recipe-213 — Field Stone Balm

**Source:** public; Herbalism level 2; tier 1; Common; DC 12; 1 active hours; 1 doses. Standard batch reference 792 gp.

**Preserved effect:** Applied over 1 minute, restores 1d6+2 hit points and treats one wound, burn, or infection appropriate to its ingredients.

**Operational effect:** After one uninterrupted active minute, attempt 1d6+2 ordinary magical nonspell HP healing under actual caps and blockers. After healing and its condition endpoints, choose at most one present local wound, burn, infection or Bleeding source appropriate to topical treatment. A Bleeding source with an existing Medicine-based removal DC permits one immediate WIS (Medicine) check against that DC using this dose as dressing, with no extra healer-kit charge. Do not attempt this if this dose already resolved a healing-triggered removal/treatment attempt for that record. Otherwise it supplies only one expressly required topical dressing/cleaning step in the source procedure; every other time, check, Supply, kit, medicine, rest and cure requirement remains. No defined interaction means no extra condition removal.

**Administration:** 1 uninterrupted active minute(s), requiring 10 consecutive regular-turn Actions in initiative and the full elapsed interval; keep touch and one hand available. Spend one actual dose at legal start. No benefit until completion; interruption does not refund it.

**Work:** Herbalist's Table; Herbalism kit, Mortar and pestle, Drying rack. Mode field; field flag true; up to 0 assistants; formula required false.

**Exact ingredients:** 1 × Medicinal herbs (component tier 1; 0.1 lb/unit; 2 gp/unit; substrate; consumed); 1 × Honey (component tier 1; 0.1 lb/unit; 2 gp/unit; seasoning; consumed); 1 × shamanic bloodstone (component tier 5; 0.14 lb/unit; 582 gp/unit; catalyst; consumed).

**Packaging:** no source vessels. Reserve 1 actual Glass vials for Standard output; 1 for Exceptional yield; 1 for full Masterwork yield. Each filled vial is 0.2 lb and one dose. At maximum yield with any eligible catalyst returned, reserve 0 lb additional clean carrier water. Owned intact spent vials may be reused; new ordinary Glass vials have a 1-gp reference price. All chosen-output packaging and carrier must be present before the check.

**Flawed:** {"mode": "treat-as-Failed", "quantity": 0, "recovery": "framework 25 percent non-catalyst inputs"}. Exceptional/Masterwork choose finite yield or Standard quantity with every container at max/current HP 2, never both. No effect potency or extra cures.

**Provenance:** current effect and original ingredient identities are retained. Legacy fields remain in source/JSON and are inactive. No source deletion.

## recipe-214 — Superior Caustic Tonic of Caustic Goo

**Source:** public; Herbalism level 5; tier 3; Common; DC 8; 8 active hours; 3 doses. Standard batch reference 301 gp.

**Preserved effect:** Grants +1 to saves and checks related to acid hazards for 10 minutes.

**Operational effect:** Gain +1 on the recipient's own qualifying checks and saves against Acid hazards for 10 elapsed minutes. Saves against actual acid-damage or corrosive hazards; checks directly handling, avoiding or disabling such a hazard. No attack/damage bonus, automatic resistance, extra save or resource recovery.

**Administration:** Action, one available hand, drink or feed a compatible willing or Incapacitated recipient within 5 feet. Spend one actual dose at legal start. No benefit until completion; interruption does not refund it.

**Work:** Herbalist's Table; Herbalism kit, Mortar and pestle, Drying rack. Mode expedition; field flag true; up to 0 assistants; formula required true.

**Exact ingredients:** 2 × Healing roots (component tier 3; 0.1 lb/unit; 25 gp/unit; substrate; consumed); 2 × Medicinal herbs (component tier 3; 0.1 lb/unit; 25 gp/unit; substrate; consumed); 4 × Dried flowers (component tier 3; 0.1 lb/unit; 25 gp/unit; substrate; consumed); 1 × caustic goo (component tier 1; 0.99 lb/unit; 8 gp/unit; material; consumed).

**Packaging:** no source vessels. Reserve 3 actual Glass vials for Standard output; 3 for Exceptional yield; 4 for full Masterwork yield. Each filled vial is 0.2 lb and one dose. At maximum yield with any eligible catalyst returned, reserve 0 lb additional clean carrier water. Owned intact spent vials may be reused; new ordinary Glass vials have a 1-gp reference price. All chosen-output packaging and carrier must be present before the check.

**Flawed:** {"mode": "half-batch-quantity", "quantity": 1, "effectChange": null}. Exceptional/Masterwork choose finite yield or Standard quantity with every container at max/current HP 2, never both. No effect potency or extra cures.

**Provenance:** current effect and original ingredient identities are retained. Legacy fields remain in source/JSON and are inactive. No source deletion.

## recipe-215 — Masterwork Resonant Tea of Black Blood

**Source:** public; Herbalism level 8; tier 4; Uncommon; DC 15; 8 active hours; 1 doses. Standard batch reference 797 gp.

**Preserved effect:** Grants +1 to saves and checks related to arcane hazards for 1 hour.

**Operational effect:** Gain +1 on the recipient's own qualifying checks and saves against Arcane hazards for 60 elapsed minutes. Explicit magical/Arcane traps, wards, fields, environmental phenomena or similar hazards; not every hostile spell or caster action. No attack/damage bonus, automatic resistance, extra save or resource recovery.

**Administration:** Action, one available hand, drink or feed a compatible willing or Incapacitated recipient within 5 feet. Spend one actual dose at legal start. No benefit until completion; interruption does not refund it.

**Work:** Herbalist's Table; Herbalism kit, Mortar and pestle, Drying rack. Mode expedition; field flag true; up to 0 assistants; formula required true.

**Exact ingredients:** 2 × Beeswax (component tier 4; 0.1 lb/unit; 75 gp/unit; binder; consumed); 1 × Dried flowers (component tier 4; 0.1 lb/unit; 75 gp/unit; substrate; consumed); 4 × Purified water (component tier 4; 0.5 lb/unit; 75 gp/unit; solvent; consumed); 1 × black blood sample (component tier 2; 0.38 lb/unit; 42 gp/unit; catalyst; consumed).

**Packaging:** no source vessels. Reserve 1 actual Glass vials for Standard output; 1 for Exceptional yield; 1 for full Masterwork yield. Each filled vial is 0.2 lb and one dose. At maximum yield with any eligible catalyst returned, reserve 0 lb additional clean carrier water. Owned intact spent vials may be reused; new ordinary Glass vials have a 1-gp reference price. All chosen-output packaging and carrier must be present before the check.

**Flawed:** {"mode": "half-fixed-duration", "durationSeconds": 1800, "instantCureUnchanged": false}. Exceptional/Masterwork choose finite yield or Standard quantity with every container at max/current HP 2, never both. No effect potency or extra cures.

**Provenance:** current effect and original ingredient identities are retained. Legacy fields remain in source/JSON and are inactive. No source deletion.

## recipe-216 — Masterwork Gale Tea of Dream Bark

**Source:** public; Herbalism level 8; tier 4; Uncommon; DC 13; 16 active hours; 1 doses. Standard batch reference 1422 gp.

**Preserved effect:** Grants +1 to saves and checks related to air hazards for 1 hour.

**Operational effect:** Gain +1 on the recipient's own qualifying checks and saves against Air hazards for 60 elapsed minutes. Hazardous wind, pressure, inhalation, air deprivation or airborne environmental force; not thunder from theme alone. No attack/damage bonus, automatic resistance, extra save or resource recovery.

**Administration:** Action, one available hand, drink or feed a compatible willing or Incapacitated recipient within 5 feet. Spend one actual dose at legal start. No benefit until completion; interruption does not refund it.

**Work:** Herbalist's Table; Herbalism kit, Mortar and pestle, Drying rack. Mode workshop; field flag false; up to 0 assistants; formula required true.

**Exact ingredients:** 5 × Purified water (component tier 4; 0.5 lb/unit; 75 gp/unit; solvent; consumed); 3 × Natural oils (component tier 4; 0.5 lb/unit; 75 gp/unit; solvent; consumed); 1 × Mortar and pestle (component tier 4; 1.0 lb/unit; 225 gp/unit; tool; returned); 5 × Beeswax (component tier 4; 0.1 lb/unit; 75 gp/unit; binder; consumed); 1 × dream bark (component tier 2; 0.45 lb/unit; 31 gp/unit; material; consumed).

**Packaging:** no source vessels. Reserve 1 actual Glass vials for Standard output; 1 for Exceptional yield; 1 for full Masterwork yield. Each filled vial is 0.2 lb and one dose. At maximum yield with any eligible catalyst returned, reserve 0 lb additional clean carrier water. Owned intact spent vials may be reused; new ordinary Glass vials have a 1-gp reference price. All chosen-output packaging and carrier must be present before the check.

**Flawed:** {"mode": "half-fixed-duration", "durationSeconds": 1800, "instantCureUnchanged": false}. Exceptional/Masterwork choose finite yield or Standard quantity with every container at max/current HP 2, never both. No effect potency or extra cures.

**Provenance:** current effect and original ingredient identities are retained. Legacy fields remain in source/JSON and are inactive. No source deletion.

## recipe-217 — Superior Mindward Compress of Eldritch Ichor

**Source:** public; Herbalism level 6; tier 3; Uncommon; DC 13; 24 active hours; 1 doses. Standard batch reference 225 gp.

**Preserved effect:** Applied over 1 minute, restores 2d6+4 hit points and treats one wound, burn, or infection appropriate to its ingredients.

**Operational effect:** After one uninterrupted active minute, attempt 2d6+4 ordinary magical nonspell HP healing under actual caps and blockers. After healing and its condition endpoints, choose at most one present local wound, burn, infection or Bleeding source appropriate to topical treatment. A Bleeding source with an existing Medicine-based removal DC permits one immediate WIS (Medicine) check against that DC using this dose as dressing, with no extra healer-kit charge. Do not attempt this if this dose already resolved a healing-triggered removal/treatment attempt for that record. Otherwise it supplies only one expressly required topical dressing/cleaning step in the source procedure; every other time, check, Supply, kit, medicine, rest and cure requirement remains. No defined interaction means no extra condition removal.

**Administration:** 1 uninterrupted active minute(s), requiring 10 consecutive regular-turn Actions in initiative and the full elapsed interval; keep touch and one hand available. Spend one actual dose at legal start. No benefit until completion; interruption does not refund it.

**Work:** Herbalist's Table; Herbalism kit, Mortar and pestle, Drying rack. Mode workshop; field flag false; up to 0 assistants; formula required true.

**Exact ingredients:** 1 × Natural oils (component tier 3; 0.5 lb/unit; 25 gp/unit; solvent; consumed); 3 × Healing roots (component tier 3; 0.1 lb/unit; 25 gp/unit; substrate; consumed); 1 × eldritch ichor (component tier 1; 0.45 lb/unit; 13 gp/unit; catalyst; consumed).

**Packaging:** no source vessels. Reserve 1 actual Glass vials for Standard output; 1 for Exceptional yield; 1 for full Masterwork yield. Each filled vial is 0.2 lb and one dose. At maximum yield with any eligible catalyst returned, reserve 0 lb additional clean carrier water. Owned intact spent vials may be reused; new ordinary Glass vials have a 1-gp reference price. All chosen-output packaging and carrier must be present before the check.

**Flawed:** {"mode": "treat-as-Failed", "quantity": 0, "recovery": "framework 25 percent non-catalyst inputs"}. Exceptional/Masterwork choose finite yield or Standard quantity with every container at max/current HP 2, never both. No effect potency or extra cures.

**Provenance:** current effect and original ingredient identities are retained. Legacy fields remain in source/JSON and are inactive. No source deletion.

## recipe-218 — Exalted Ember Powder of Glimmering Leaf

**Source:** public; Herbalism level 10; tier 5; Uncommon; DC 17; 8 active hours; 1 doses. Standard batch reference 3041 gp.

**Preserved effect:** Grants +1 to saves and checks related to fire hazards for 1 hour.

**Operational effect:** Gain +1 on the recipient's own qualifying checks and saves against Fire hazards for 60 elapsed minutes. Saves against actual fire-damage or fire environmental hazards; checks directly avoiding, extinguishing or safely traversing a fire hazard. No attack/damage bonus, automatic resistance, extra save or resource recovery.

**Administration:** Action, one available hand, drink or feed a compatible willing or Incapacitated recipient within 5 feet. Spend one actual dose at legal start. No benefit until completion; interruption does not refund it.

**Work:** Herbalist's Table; Herbalism kit, Mortar and pestle, Drying rack. Mode expedition; field flag true; up to 0 assistants; formula required true.

**Exact ingredients:** 5 × Dried flowers (component tier 5; 0.1 lb/unit; 200 gp/unit; substrate; consumed); 2 × Healing roots (component tier 5; 0.1 lb/unit; 200 gp/unit; substrate; consumed); 1 × Beeswax (component tier 5; 0.1 lb/unit; 200 gp/unit; binder; consumed); 3 × Purified water (component tier 5; 0.5 lb/unit; 200 gp/unit; solvent; consumed); 1 × glimmering leaf (component tier 2; 0.75 lb/unit; 23 gp/unit; material; consumed).

**Packaging:** no source vessels. Reserve 1 actual Glass vials for Standard output; 1 for Exceptional yield; 1 for full Masterwork yield. Each filled vial is 0.2 lb and one dose. At maximum yield with any eligible catalyst returned, reserve 0 lb additional clean carrier water. Owned intact spent vials may be reused; new ordinary Glass vials have a 1-gp reference price. All chosen-output packaging and carrier must be present before the check.

**Flawed:** {"mode": "half-fixed-duration", "durationSeconds": 1800, "instantCureUnchanged": false}. Exceptional/Masterwork choose finite yield or Standard quantity with every container at max/current HP 2, never both. No effect potency or extra cures.

**Provenance:** current effect and original ingredient identities are retained. Legacy fields remain in source/JSON and are inactive. No source deletion.

## recipe-219 — Superior Ember Remedy of Dream Bark

**Source:** public; Herbalism level 6; tier 3; Uncommon; DC 16; 24 active hours; 1 doses. Standard batch reference 688 gp.

**Preserved effect:** Grants +1 to saves and checks related to fire hazards for 1 hour.

**Operational effect:** Gain +1 on the recipient's own qualifying checks and saves against Fire hazards for 60 elapsed minutes. Saves against actual fire-damage or fire environmental hazards; checks directly avoiding, extinguishing or safely traversing a fire hazard. No attack/damage bonus, automatic resistance, extra save or resource recovery.

**Administration:** Action, one available hand, drink or feed a compatible willing or Incapacitated recipient within 5 feet. Spend one actual dose at legal start. No benefit until completion; interruption does not refund it.

**Work:** Herbalist's Table; Herbalism kit, Mortar and pestle, Drying rack. Mode workshop; field flag false; up to 0 assistants; formula required true.

**Exact ingredients:** 4 × Honey (component tier 3; 0.1 lb/unit; 25 gp/unit; seasoning; consumed); 3 × Natural oils (component tier 3; 0.5 lb/unit; 25 gp/unit; solvent; consumed); 5 × Healing roots (component tier 3; 0.1 lb/unit; 25 gp/unit; substrate; consumed); 5 × Crushed leaves (component tier 3; 0.1 lb/unit; 25 gp/unit; ingredient; consumed); 1 × dream bark (component tier 2; 0.45 lb/unit; 31 gp/unit; material; consumed).

**Packaging:** no source vessels. Reserve 1 actual Glass vials for Standard output; 1 for Exceptional yield; 1 for full Masterwork yield. Each filled vial is 0.2 lb and one dose. At maximum yield with any eligible catalyst returned, reserve 0 lb additional clean carrier water. Owned intact spent vials may be reused; new ordinary Glass vials have a 1-gp reference price. All chosen-output packaging and carrier must be present before the check.

**Flawed:** {"mode": "half-fixed-duration", "durationSeconds": 1800, "instantCureUnchanged": false}. Exceptional/Masterwork choose finite yield or Standard quantity with every container at max/current HP 2, never both. No effect potency or extra cures.

**Provenance:** current effect and original ingredient identities are retained. Legacy fields remain in source/JSON and are inactive. No source deletion.

## recipe-220 — Exalted Vital Antidote of Black Blood

**Source:** public; Herbalism level 9; tier 5; Uncommon; DC 14; 8 active hours; 1 doses. Standard batch reference 3873 gp.

**Preserved effect:** Ends the poisoned condition and grants advantage on saves against poison for 1 hour.

**Operational effect:** End every present removable Poisoned application, without deleting its independent underlying cause; future exposure may reapply it. Gain advantage on saves against poison for 60 elapsed minutes. No added numeric bonus, poison immunity, resistance, disease or intoxication cure.

**Administration:** Action, one available hand, drink or feed a compatible willing or Incapacitated recipient within 5 feet. Spend one actual dose at legal start. No benefit until completion; interruption does not refund it.

**Work:** Herbalist's Table; Herbalism kit, Mortar and pestle, Drying rack. Mode expedition; field flag true; up to 0 assistants; formula required true.

**Exact ingredients:** 4 × Honey (component tier 5; 0.1 lb/unit; 200 gp/unit; seasoning; consumed); 5 × Medicinal herbs (component tier 5; 0.1 lb/unit; 200 gp/unit; substrate; consumed); 5 × Beeswax (component tier 5; 0.1 lb/unit; 200 gp/unit; binder; consumed); 1 × black blood sample (component tier 2; 0.38 lb/unit; 42 gp/unit; catalyst; consumed).

**Packaging:** no source vessels. Reserve 1 actual Glass vials for Standard output; 1 for Exceptional yield; 1 for full Masterwork yield. Each filled vial is 0.2 lb and one dose. At maximum yield with any eligible catalyst returned, reserve 0 lb additional clean carrier water. Owned intact spent vials may be reused; new ordinary Glass vials have a 1-gp reference price. All chosen-output packaging and carrier must be present before the check.

**Flawed:** {"mode": "half-fixed-duration", "durationSeconds": 1800, "instantCureUnchanged": true}. Exceptional/Masterwork choose finite yield or Standard quantity with every container at max/current HP 2, never both. No effect potency or extra cures.

**Provenance:** current effect and original ingredient identities are retained. Legacy fields remain in source/JSON and are inactive. No source deletion.

## recipe-221 — Masterwork Ember Healing Salve of Glimmering Leaf

**Source:** public; Herbalism level 8; tier 4; Uncommon; DC 16; 16 active hours; 1 doses. Standard batch reference 500 gp.

**Preserved effect:** Applied over 1 minute, restores 2d6+4 hit points and treats one wound, burn, or infection appropriate to its ingredients.

**Operational effect:** After one uninterrupted active minute, attempt 2d6+4 ordinary magical nonspell HP healing under actual caps and blockers. After healing and its condition endpoints, choose at most one present local wound, burn, infection or Bleeding source appropriate to topical treatment. A Bleeding source with an existing Medicine-based removal DC permits one immediate WIS (Medicine) check against that DC using this dose as dressing, with no extra healer-kit charge. Do not attempt this if this dose already resolved a healing-triggered removal/treatment attempt for that record. Otherwise it supplies only one expressly required topical dressing/cleaning step in the source procedure; every other time, check, Supply, kit, medicine, rest and cure requirement remains. No defined interaction means no extra condition removal.

**Administration:** 1 uninterrupted active minute(s), requiring 10 consecutive regular-turn Actions in initiative and the full elapsed interval; keep touch and one hand available. Spend one actual dose at legal start. No benefit until completion; interruption does not refund it.

**Work:** Herbalist's Table; Herbalism kit, Mortar and pestle, Drying rack. Mode workshop; field flag false; up to 0 assistants; formula required true.

**Exact ingredients:** 3 × Natural oils (component tier 4; 0.5 lb/unit; 75 gp/unit; solvent; consumed); 1 × Healing roots (component tier 4; 0.1 lb/unit; 75 gp/unit; substrate; consumed); 1 × glimmering leaf (component tier 2; 0.75 lb/unit; 23 gp/unit; material; consumed).

**Packaging:** no source vessels. Reserve 1 actual Glass vials for Standard output; 1 for Exceptional yield; 1 for full Masterwork yield. Each filled vial is 0.2 lb and one dose. At maximum yield with any eligible catalyst returned, reserve 0 lb additional clean carrier water. Owned intact spent vials may be reused; new ordinary Glass vials have a 1-gp reference price. All chosen-output packaging and carrier must be present before the check.

**Flawed:** {"mode": "treat-as-Failed", "quantity": 0, "recovery": "framework 25 percent non-catalyst inputs"}. Exceptional/Masterwork choose finite yield or Standard quantity with every container at max/current HP 2, never both. No effect potency or extra cures.

**Provenance:** current effect and original ingredient identities are retained. Legacy fields remain in source/JSON and are inactive. No source deletion.

## recipe-222 — Superior Veiled Powder of Black Blood

**Source:** public; Herbalism level 5; tier 3; Uncommon; DC 14; 16 active hours; 1 doses. Standard batch reference 333 gp.

**Preserved effect:** Grants +1 to saves and checks related to stealth hazards for 1 hour.

**Operational effect:** Gain +1 on the recipient's own qualifying checks and saves against Stealth hazards for 60 elapsed minutes. Stealth checks to avoid detection by a present hostile observer, pursuer, guard, sensor or hazard-detection system; no Deception, Initiative, attack bonus or automatic Hidden state. No attack/damage bonus, automatic resistance, extra save or resource recovery.

**Administration:** Action, one available hand, drink or feed a compatible willing or Incapacitated recipient within 5 feet. Spend one actual dose at legal start. No benefit until completion; interruption does not refund it.

**Work:** Herbalist's Table; Herbalism kit, Mortar and pestle, Drying rack. Mode workshop; field flag false; up to 0 assistants; formula required true.

**Exact ingredients:** 2 × Healing roots (component tier 3; 0.1 lb/unit; 25 gp/unit; substrate; consumed); 3 × Crushed leaves (component tier 3; 0.1 lb/unit; 25 gp/unit; ingredient; consumed); 2 × Beeswax (component tier 3; 0.1 lb/unit; 25 gp/unit; binder; consumed); 1 × black blood sample (component tier 2; 0.38 lb/unit; 42 gp/unit; catalyst; consumed).

**Packaging:** no source vessels. Reserve 1 actual Glass vials for Standard output; 1 for Exceptional yield; 1 for full Masterwork yield. Each filled vial is 0.2 lb and one dose. At maximum yield with any eligible catalyst returned, reserve 0 lb additional clean carrier water. Owned intact spent vials may be reused; new ordinary Glass vials have a 1-gp reference price. All chosen-output packaging and carrier must be present before the check.

**Flawed:** {"mode": "half-fixed-duration", "durationSeconds": 1800, "instantCureUnchanged": false}. Exceptional/Masterwork choose finite yield or Standard quantity with every container at max/current HP 2, never both. No effect potency or extra cures.

**Provenance:** current effect and original ingredient identities are retained. Legacy fields remain in source/JSON and are inactive. No source deletion.

## recipe-223 — Exalted Storm Powder of Sparkling Petal

**Source:** public; Herbalism level 9; tier 5; Uncommon; DC 14; 16 active hours; 1 doses. Standard batch reference 2246 gp.

**Preserved effect:** Grants +1 to saves and checks related to lightning hazards for 1 hour.

**Operational effect:** Gain +1 on the recipient's own qualifying checks and saves against Lightning hazards for 60 elapsed minutes. Saves against actual lightning-damage or electrical hazards; checks directly identifying, avoiding or disabling such a hazard. No attack/damage bonus, automatic resistance, extra save or resource recovery.

**Administration:** Action, one available hand, drink or feed a compatible willing or Incapacitated recipient within 5 feet. Spend one actual dose at legal start. No benefit until completion; interruption does not refund it.

**Work:** Herbalist's Table; Herbalism kit, Mortar and pestle, Drying rack. Mode workshop; field flag false; up to 0 assistants; formula required true.

**Exact ingredients:** 2 × Honey (component tier 5; 0.1 lb/unit; 200 gp/unit; seasoning; consumed); 4 × Healing roots (component tier 5; 0.1 lb/unit; 200 gp/unit; substrate; consumed); 2 × Dried flowers (component tier 5; 0.1 lb/unit; 200 gp/unit; substrate; consumed); 1 × sparkling petal (component tier 1; 0.36 lb/unit; 10 gp/unit; material; consumed).

**Packaging:** no source vessels. Reserve 1 actual Glass vials for Standard output; 1 for Exceptional yield; 1 for full Masterwork yield. Each filled vial is 0.2 lb and one dose. At maximum yield with any eligible catalyst returned, reserve 0 lb additional clean carrier water. Owned intact spent vials may be reused; new ordinary Glass vials have a 1-gp reference price. All chosen-output packaging and carrier must be present before the check.

**Flawed:** {"mode": "half-fixed-duration", "durationSeconds": 1800, "instantCureUnchanged": false}. Exceptional/Masterwork choose finite yield or Standard quantity with every container at max/current HP 2, never both. No effect potency or extra cures.

**Provenance:** current effect and original ingredient identities are retained. Legacy fields remain in source/JSON and are inactive. No source deletion.

## recipe-224 — Masterwork Mighty Tea of Poisonous Sinew

**Source:** public; Herbalism level 8; tier 4; Uncommon; DC 15; 8 active hours; 1 doses. Standard batch reference 425 gp.

**Preserved effect:** Grants +1 to saves and checks related to strength hazards for 1 hour.

**Operational effect:** Gain +1 on the recipient's own qualifying checks and saves against Strength hazards for 60 elapsed minutes. STR checks and saves to resist or escape an actual physical hazard, restraint, crushing force, forced movement or entrapment; not attacks, damage, carrying capacity or every STR roll. No attack/damage bonus, automatic resistance, extra save or resource recovery.

**Administration:** Action, one available hand, drink or feed a compatible willing or Incapacitated recipient within 5 feet. Spend one actual dose at legal start. No benefit until completion; interruption does not refund it.

**Work:** Herbalist's Table; Herbalism kit, Mortar and pestle, Drying rack. Mode expedition; field flag true; up to 0 assistants; formula required true.

**Exact ingredients:** 1 × Mortar and pestle (component tier 4; 1.0 lb/unit; 225 gp/unit; tool; returned); 1 × Medicinal herbs (component tier 4; 0.1 lb/unit; 75 gp/unit; substrate; consumed); 2 × Natural oils (component tier 4; 0.5 lb/unit; 75 gp/unit; solvent; consumed); 1 × Poisonous sinew (component tier 3; 0.38 lb/unit; 66 gp/unit; catalyst; consumed).

**Packaging:** no source vessels. Reserve 1 actual Glass vials for Standard output; 1 for Exceptional yield; 1 for full Masterwork yield. Each filled vial is 0.2 lb and one dose. At maximum yield with any eligible catalyst returned, reserve 0 lb additional clean carrier water. Owned intact spent vials may be reused; new ordinary Glass vials have a 1-gp reference price. All chosen-output packaging and carrier must be present before the check.

**Flawed:** {"mode": "half-fixed-duration", "durationSeconds": 1800, "instantCureUnchanged": false}. Exceptional/Masterwork choose finite yield or Standard quantity with every container at max/current HP 2, never both. No effect potency or extra cures.

**Provenance:** current effect and original ingredient identities are retained. Legacy fields remain in source/JSON and are inactive. No source deletion.

## recipe-225 — Exalted Vital Compress of Black Blood

**Source:** public; Herbalism level 10; tier 5; Rare; DC 18; 40 active hours; 1 doses. Standard batch reference 1607 gp.

**Preserved effect:** Applied over 1 minute, restores 4d6+6 hit points and treats one wound, burn, or infection appropriate to its ingredients.

**Operational effect:** After one uninterrupted active minute, attempt 4d6+6 ordinary magical nonspell HP healing under actual caps and blockers. After healing and its condition endpoints, choose at most one present local wound, burn, infection or Bleeding source appropriate to topical treatment. A Bleeding source with an existing Medicine-based removal DC permits one immediate WIS (Medicine) check against that DC using this dose as dressing, with no extra healer-kit charge. Do not attempt this if this dose already resolved a healing-triggered removal/treatment attempt for that record. Otherwise it supplies only one expressly required topical dressing/cleaning step in the source procedure; every other time, check, Supply, kit, medicine, rest and cure requirement remains. No defined interaction means no extra condition removal.

**Administration:** 1 uninterrupted active minute(s), requiring 10 consecutive regular-turn Actions in initiative and the full elapsed interval; keep touch and one hand available. Spend one actual dose at legal start. No benefit until completion; interruption does not refund it.

**Work:** Herbalist's Table; Herbalism kit, Mortar and pestle, Drying rack. Mode workshop; field flag false; up to 0 assistants; formula required true.

**Exact ingredients:** 1 × Mortar and pestle (component tier 5; 1.0 lb/unit; 600 gp/unit; tool; returned); 4 × Honey (component tier 5; 0.1 lb/unit; 200 gp/unit; seasoning; consumed); 1 × Healing roots (component tier 5; 0.1 lb/unit; 200 gp/unit; substrate; consumed); 1 × black blood sample (component tier 2; 0.38 lb/unit; 42 gp/unit; catalyst; consumed).

**Packaging:** no source vessels. Reserve 1 actual Glass vials for Standard output; 1 for Exceptional yield; 1 for full Masterwork yield. Each filled vial is 0.2 lb and one dose. At maximum yield with any eligible catalyst returned, reserve 0 lb additional clean carrier water. Owned intact spent vials may be reused; new ordinary Glass vials have a 1-gp reference price. All chosen-output packaging and carrier must be present before the check.

**Flawed:** {"mode": "treat-as-Failed", "quantity": 0, "recovery": "framework 25 percent non-catalyst inputs"}. Exceptional/Masterwork choose finite yield or Standard quantity with every container at max/current HP 2, never both. No effect potency or extra cures.

**Provenance:** current effect and original ingredient identities are retained. Legacy fields remain in source/JSON and are inactive. No source deletion.

## recipe-226 — Legendary Venom Compress of Poisonous Sinew

**Source:** restricted; Herbalism level 11; tier 6; Rare; DC 20; 80 active hours; 1 doses. Standard batch reference 14029 gp.

**Preserved effect:** Applied over 1 minute, restores 4d6+6 hit points and treats one wound, burn, or infection appropriate to its ingredients.

**Operational effect:** After one uninterrupted active minute, attempt 4d6+6 ordinary magical nonspell HP healing under actual caps and blockers. After healing and its condition endpoints, choose at most one present local wound, burn, infection or Bleeding source appropriate to topical treatment. A Bleeding source with an existing Medicine-based removal DC permits one immediate WIS (Medicine) check against that DC using this dose as dressing, with no extra healer-kit charge. Do not attempt this if this dose already resolved a healing-triggered removal/treatment attempt for that record. Otherwise it supplies only one expressly required topical dressing/cleaning step in the source procedure; every other time, check, Supply, kit, medicine, rest and cure requirement remains. No defined interaction means no extra condition removal.

**Administration:** 1 uninterrupted active minute(s), requiring 10 consecutive regular-turn Actions in initiative and the full elapsed interval; keep touch and one hand available. Spend one actual dose at legal start. No benefit until completion; interruption does not refund it.

**Work:** Herbalist's Table; Herbalism kit, Mortar and pestle, Drying rack. Mode haven; field flag false; up to 0 assistants; formula required true.

**Exact ingredients:** 5 × Honey (component tier 6; 0.1 lb/unit; 500 gp/unit; seasoning; consumed); 4 × Healing roots (component tier 6; 0.1 lb/unit; 500 gp/unit; substrate; consumed); 5 × Dried flowers (component tier 6; 0.1 lb/unit; 500 gp/unit; substrate; consumed); 5 × Beeswax (component tier 6; 0.1 lb/unit; 500 gp/unit; binder; consumed); 1 × Crushed leaves (component tier 6; 0.1 lb/unit; 500 gp/unit; ingredient; consumed); 1 × Poisonous sinew (component tier 3; 0.38 lb/unit; 66 gp/unit; catalyst; consumed).

**Packaging:** no source vessels. Reserve 1 actual Glass vials for Standard output; 1 for Exceptional yield; 1 for full Masterwork yield. Each filled vial is 0.2 lb and one dose. At maximum yield with any eligible catalyst returned, reserve 0 lb additional clean carrier water. Owned intact spent vials may be reused; new ordinary Glass vials have a 1-gp reference price. All chosen-output packaging and carrier must be present before the check.

**Flawed:** {"mode": "treat-as-Failed", "quantity": 0, "recovery": "framework 25 percent non-catalyst inputs"}. Exceptional/Masterwork choose finite yield or Standard quantity with every container at max/current HP 2, never both. No effect potency or extra cures.

**Provenance:** current effect and original ingredient identities are retained. Legacy fields remain in source/JSON and are inactive. No source deletion.

## recipe-227 — Legendary Resonant Powder of Poisonous Sinew

**Source:** restricted; Herbalism level 12; tier 6; Rare; DC 18; 80 active hours; 1 doses. Standard batch reference 9344 gp.

**Preserved effect:** Grants +2 to saves and checks related to arcane hazards for 4 hours.

**Operational effect:** Gain +2 on the recipient's own qualifying checks and saves against Arcane hazards for 240 elapsed minutes. Explicit magical/Arcane traps, wards, fields, environmental phenomena or similar hazards; not every hostile spell or caster action. No attack/damage bonus, automatic resistance, extra save or resource recovery.

**Administration:** Action, one available hand, drink or feed a compatible willing or Incapacitated recipient within 5 feet. Spend one actual dose at legal start. No benefit until completion; interruption does not refund it.

**Work:** Herbalist's Table; Herbalism kit, Mortar and pestle, Drying rack. Mode haven; field flag false; up to 1 assistants; formula required true.

**Exact ingredients:** 1 × Mortar and pestle (component tier 6; 1.0 lb/unit; 1500 gp/unit; tool; returned); 3 × Crushed leaves (component tier 6; 0.1 lb/unit; 500 gp/unit; ingredient; consumed); 4 × Healing roots (component tier 6; 0.1 lb/unit; 500 gp/unit; substrate; consumed); 1 × Medicinal herbs (component tier 6; 0.1 lb/unit; 500 gp/unit; substrate; consumed); 5 × Natural oils (component tier 6; 0.5 lb/unit; 500 gp/unit; solvent; consumed); 1 × Poisonous sinew (component tier 3; 0.38 lb/unit; 66 gp/unit; catalyst; consumed).

**Packaging:** no source vessels. Reserve 1 actual Glass vials for Standard output; 1 for Exceptional yield; 1 for full Masterwork yield. Each filled vial is 0.2 lb and one dose. At maximum yield with any eligible catalyst returned, reserve 0 lb additional clean carrier water. Owned intact spent vials may be reused; new ordinary Glass vials have a 1-gp reference price. All chosen-output packaging and carrier must be present before the check.

**Flawed:** {"mode": "half-fixed-duration", "durationSeconds": 7200, "instantCureUnchanged": false}. Exceptional/Masterwork choose finite yield or Standard quantity with every container at max/current HP 2, never both. No effect potency or extra cures.

**Provenance:** current effect and original ingredient identities are retained. Legacy fields remain in source/JSON and are inactive. No source deletion.

## recipe-228 — Exalted Vital Powder of Black Blood

**Source:** public; Herbalism level 10; tier 5; Rare; DC 19; 80 active hours; 1 doses. Standard batch reference 5047 gp.

**Preserved effect:** Grants +2 to saves and checks related to vitality hazards for 4 hours.

**Operational effect:** Gain +2 on the recipient's own qualifying checks and saves against Vitality hazards for 240 elapsed minutes. CON checks and saves against fatigue, exposure, environmental endurance or disease hazards; never death saves, concentration, Wound/Injury saves or an additional recovery roll. No attack/damage bonus, automatic resistance, extra save or resource recovery.

**Administration:** Action, one available hand, drink or feed a compatible willing or Incapacitated recipient within 5 feet. Spend one actual dose at legal start. No benefit until completion; interruption does not refund it.

**Work:** Herbalist's Table; Herbalism kit, Mortar and pestle, Drying rack. Mode haven; field flag false; up to 0 assistants; formula required true.

**Exact ingredients:** 5 × Crushed leaves (component tier 5; 0.1 lb/unit; 200 gp/unit; ingredient; consumed); 1 × Natural oils (component tier 5; 0.5 lb/unit; 200 gp/unit; solvent; consumed); 5 × Purified water (component tier 5; 0.5 lb/unit; 200 gp/unit; solvent; consumed); 4 × Medicinal herbs (component tier 5; 0.1 lb/unit; 200 gp/unit; substrate; consumed); 2 × Beeswax (component tier 5; 0.1 lb/unit; 200 gp/unit; binder; consumed); 1 × black blood sample (component tier 2; 0.38 lb/unit; 42 gp/unit; catalyst; consumed).

**Packaging:** no source vessels. Reserve 1 actual Glass vials for Standard output; 1 for Exceptional yield; 1 for full Masterwork yield. Each filled vial is 0.2 lb and one dose. At maximum yield with any eligible catalyst returned, reserve 0 lb additional clean carrier water. Owned intact spent vials may be reused; new ordinary Glass vials have a 1-gp reference price. All chosen-output packaging and carrier must be present before the check.

**Flawed:** {"mode": "half-fixed-duration", "durationSeconds": 7200, "instantCureUnchanged": false}. Exceptional/Masterwork choose finite yield or Standard quantity with every container at max/current HP 2, never both. No effect potency or extra cures.

**Provenance:** current effect and original ingredient identities are retained. Legacy fields remain in source/JSON and are inactive. No source deletion.

## recipe-229 — Relic Ember Tonic of Poisonous Sinew

**Source:** director-only; Herbalism level 13; tier 7; Rare; DC 19; 40 active hours; 1 doses. Standard batch reference 24649 gp.

**Preserved effect:** Grants +2 to saves and checks related to fire hazards for 4 hours.

**Operational effect:** Gain +2 on the recipient's own qualifying checks and saves against Fire hazards for 240 elapsed minutes. Saves against actual fire-damage or fire environmental hazards; checks directly avoiding, extinguishing or safely traversing a fire hazard. No attack/damage bonus, automatic resistance, extra save or resource recovery.

**Administration:** Action, one available hand, drink or feed a compatible willing or Incapacitated recipient within 5 feet. Spend one actual dose at legal start. No benefit until completion; interruption does not refund it.

**Work:** Herbalist's Table; Herbalism kit, Mortar and pestle, Drying rack. Mode workshop; field flag false; up to 1 assistants; formula required true.

**Exact ingredients:** 5 × Healing roots (component tier 7; 0.1 lb/unit; 1200 gp/unit; substrate; consumed); 1 × Honey (component tier 7; 0.1 lb/unit; 1200 gp/unit; seasoning; consumed); 5 × Medicinal herbs (component tier 7; 0.1 lb/unit; 1200 gp/unit; substrate; consumed); 2 × Crushed leaves (component tier 7; 0.1 lb/unit; 1200 gp/unit; ingredient; consumed); 2 × Purified water (component tier 7; 0.5 lb/unit; 1200 gp/unit; solvent; consumed); 1 × Poisonous sinew (component tier 3; 0.38 lb/unit; 66 gp/unit; catalyst; consumed).

**Packaging:** no source vessels. Reserve 1 actual Glass vials for Standard output; 1 for Exceptional yield; 1 for full Masterwork yield. Each filled vial is 0.2 lb and one dose. At maximum yield with any eligible catalyst returned, reserve 0 lb additional clean carrier water. Owned intact spent vials may be reused; new ordinary Glass vials have a 1-gp reference price. All chosen-output packaging and carrier must be present before the check.

**Flawed:** {"mode": "half-fixed-duration", "durationSeconds": 7200, "instantCureUnchanged": false}. Exceptional/Masterwork choose finite yield or Standard quantity with every container at max/current HP 2, never both. No effect potency or extra cures.

**Provenance:** current effect and original ingredient identities are retained. Legacy fields remain in source/JSON and are inactive. No source deletion.

## recipe-230 — Legendary Stone Compress of Shamanic Bloodstone

**Source:** restricted; Herbalism level 12; tier 6; Rare; DC 19; 80 active hours; 1 doses. Standard batch reference 6666 gp.

**Preserved effect:** Applied over 1 minute, restores 4d6+6 hit points and treats one wound, burn, or infection appropriate to its ingredients.

**Operational effect:** After one uninterrupted active minute, attempt 4d6+6 ordinary magical nonspell HP healing under actual caps and blockers. After healing and its condition endpoints, choose at most one present local wound, burn, infection or Bleeding source appropriate to topical treatment. A Bleeding source with an existing Medicine-based removal DC permits one immediate WIS (Medicine) check against that DC using this dose as dressing, with no extra healer-kit charge. Do not attempt this if this dose already resolved a healing-triggered removal/treatment attempt for that record. Otherwise it supplies only one expressly required topical dressing/cleaning step in the source procedure; every other time, check, Supply, kit, medicine, rest and cure requirement remains. No defined interaction means no extra condition removal.

**Administration:** 1 uninterrupted active minute(s), requiring 10 consecutive regular-turn Actions in initiative and the full elapsed interval; keep touch and one hand available. Spend one actual dose at legal start. No benefit until completion; interruption does not refund it.

**Work:** Herbalist's Table; Herbalism kit, Mortar and pestle, Drying rack. Mode haven; field flag false; up to 1 assistants; formula required true.

**Exact ingredients:** 2 × Beeswax (component tier 6; 0.1 lb/unit; 500 gp/unit; binder; consumed); 5 × Dried flowers (component tier 6; 0.1 lb/unit; 500 gp/unit; substrate; consumed); 1 × Mortar and pestle (component tier 6; 1.0 lb/unit; 1500 gp/unit; tool; returned); 1 × Crushed leaves (component tier 6; 0.1 lb/unit; 500 gp/unit; ingredient; consumed); 1 × shamanic bloodstone (component tier 5; 0.14 lb/unit; 582 gp/unit; catalyst; consumed).

**Packaging:** no source vessels. Reserve 1 actual Glass vials for Standard output; 1 for Exceptional yield; 1 for full Masterwork yield. Each filled vial is 0.2 lb and one dose. At maximum yield with any eligible catalyst returned, reserve 0 lb additional clean carrier water. Owned intact spent vials may be reused; new ordinary Glass vials have a 1-gp reference price. All chosen-output packaging and carrier must be present before the check.

**Flawed:** {"mode": "treat-as-Failed", "quantity": 0, "recovery": "framework 25 percent non-catalyst inputs"}. Exceptional/Masterwork choose finite yield or Standard quantity with every container at max/current HP 2, never both. No effect potency or extra cures.

**Provenance:** current effect and original ingredient identities are retained. Legacy fields remain in source/JSON and are inactive. No source deletion.

## recipe-231 — Relic Resonant Balm of Poisonous Sinew

**Source:** director-only; Herbalism level 14; tier 7; Rare; DC 18; 40 active hours; 1 doses. Standard batch reference 19809 gp.

**Preserved effect:** Applied over 1 minute, restores 4d6+6 hit points and treats one wound, burn, or infection appropriate to its ingredients.

**Operational effect:** After one uninterrupted active minute, attempt 4d6+6 ordinary magical nonspell HP healing under actual caps and blockers. After healing and its condition endpoints, choose at most one present local wound, burn, infection or Bleeding source appropriate to topical treatment. A Bleeding source with an existing Medicine-based removal DC permits one immediate WIS (Medicine) check against that DC using this dose as dressing, with no extra healer-kit charge. Do not attempt this if this dose already resolved a healing-triggered removal/treatment attempt for that record. Otherwise it supplies only one expressly required topical dressing/cleaning step in the source procedure; every other time, check, Supply, kit, medicine, rest and cure requirement remains. No defined interaction means no extra condition removal.

**Administration:** 1 uninterrupted active minute(s), requiring 10 consecutive regular-turn Actions in initiative and the full elapsed interval; keep touch and one hand available. Spend one actual dose at legal start. No benefit until completion; interruption does not refund it.

**Work:** Herbalist's Table; Herbalism kit, Mortar and pestle, Drying rack. Mode workshop; field flag false; up to 1 assistants; formula required true.

**Exact ingredients:** 3 × Natural oils (component tier 7; 0.5 lb/unit; 1200 gp/unit; solvent; consumed); 4 × Honey (component tier 7; 0.1 lb/unit; 1200 gp/unit; seasoning; consumed); 5 × Purified water (component tier 7; 0.5 lb/unit; 1200 gp/unit; solvent; consumed); 1 × Poisonous sinew (component tier 3; 0.38 lb/unit; 66 gp/unit; catalyst; consumed).

**Packaging:** no source vessels. Reserve 1 actual Glass vials for Standard output; 1 for Exceptional yield; 1 for full Masterwork yield. Each filled vial is 0.2 lb and one dose. At maximum yield with any eligible catalyst returned, reserve 0 lb additional clean carrier water. Owned intact spent vials may be reused; new ordinary Glass vials have a 1-gp reference price. All chosen-output packaging and carrier must be present before the check.

**Flawed:** {"mode": "treat-as-Failed", "quantity": 0, "recovery": "framework 25 percent non-catalyst inputs"}. Exceptional/Masterwork choose finite yield or Standard quantity with every container at max/current HP 2, never both. No effect potency or extra cures.

**Provenance:** current effect and original ingredient identities are retained. Legacy fields remain in source/JSON and are inactive. No source deletion.

## recipe-232 — Ascendant Caustic Compress of Poisonous Sinew

**Source:** director-only; Herbalism level 17; tier 9; Very Rare; DC 20; 160 active hours; 1 doses. Standard batch reference 122960 gp.

**Preserved effect:** Applied over 1 minute, restores 6d6+8 hit points and treats one wound, burn, or infection appropriate to its ingredients.

**Operational effect:** After one uninterrupted active minute, attempt 6d6+8 ordinary magical nonspell HP healing under actual caps and blockers. After healing and its condition endpoints, choose at most one present local wound, burn, infection or Bleeding source appropriate to topical treatment. A Bleeding source with an existing Medicine-based removal DC permits one immediate WIS (Medicine) check against that DC using this dose as dressing, with no extra healer-kit charge. Do not attempt this if this dose already resolved a healing-triggered removal/treatment attempt for that record. Otherwise it supplies only one expressly required topical dressing/cleaning step in the source procedure; every other time, check, Supply, kit, medicine, rest and cure requirement remains. No defined interaction means no extra condition removal.

**Administration:** 1 uninterrupted active minute(s), requiring 10 consecutive regular-turn Actions in initiative and the full elapsed interval; keep touch and one hand available. Spend one actual dose at legal start. No benefit until completion; interruption does not refund it.

**Work:** Herbalist's Table; Herbalism kit, Mortar and pestle, Drying rack. Mode haven; field flag false; up to 2 assistants; formula required true.

**Exact ingredients:** 3 × Dried flowers (component tier 9; 0.1 lb/unit; 7500 gp/unit; substrate; consumed); 1 × Mortar and pestle (component tier 9; 1.0 lb/unit; 22500 gp/unit; tool; returned); 2 × Medicinal herbs (component tier 9; 0.1 lb/unit; 7500 gp/unit; substrate; consumed); 1 × Beeswax (component tier 9; 0.1 lb/unit; 7500 gp/unit; binder; consumed); 3 × Purified water (component tier 9; 0.5 lb/unit; 7500 gp/unit; solvent; consumed); 3 × Honey (component tier 9; 0.1 lb/unit; 7500 gp/unit; seasoning; consumed); 1 × Poisonous sinew (component tier 3; 0.38 lb/unit; 66 gp/unit; catalyst; consumed); 1 × caustic goo (component tier 1; 0.99 lb/unit; 8 gp/unit; material; consumed).

**Packaging:** no source vessels. Reserve 1 actual Glass vials for Standard output; 1 for Exceptional yield; 1 for full Masterwork yield. Each filled vial is 0.2 lb and one dose. At maximum yield with any eligible catalyst returned, reserve 0 lb additional clean carrier water. Owned intact spent vials may be reused; new ordinary Glass vials have a 1-gp reference price. All chosen-output packaging and carrier must be present before the check.

**Flawed:** {"mode": "treat-as-Failed", "quantity": 0, "recovery": "framework 25 percent non-catalyst inputs"}. Exceptional/Masterwork choose finite yield or Standard quantity with every container at max/current HP 2, never both. No effect potency or extra cures.

**Provenance:** current effect and original ingredient identities are retained. Legacy fields remain in source/JSON and are inactive. No source deletion.

## recipe-233 — Mythic Storm Tonic of Shamanic Bloodstone

**Source:** director-only; Herbalism level 15; tier 8; Very Rare; DC 22; 120 active hours; 1 doses. Standard batch reference 42199 gp.

**Preserved effect:** Grants +2 to saves and checks related to lightning hazards for 8 hours.

**Operational effect:** Gain +2 on the recipient's own qualifying checks and saves against Lightning hazards for 480 elapsed minutes. Saves against actual lightning-damage or electrical hazards; checks directly identifying, avoiding or disabling such a hazard. No attack/damage bonus, automatic resistance, extra save or resource recovery.

**Administration:** Action, one available hand, drink or feed a compatible willing or Incapacitated recipient within 5 feet. Spend one actual dose at legal start. No benefit until completion; interruption does not refund it.

**Work:** Herbalist's Table; Herbalism kit, Mortar and pestle, Drying rack. Mode haven; field flag false; up to 1 assistants; formula required true.

**Exact ingredients:** 3 × Natural oils (component tier 8; 0.5 lb/unit; 3000 gp/unit; solvent; consumed); 1 × Dried flowers (component tier 8; 0.1 lb/unit; 3000 gp/unit; substrate; consumed); 4 × Crushed leaves (component tier 8; 0.1 lb/unit; 3000 gp/unit; ingredient; consumed); 2 × Beeswax (component tier 8; 0.1 lb/unit; 3000 gp/unit; binder; consumed); 1 × shamanic bloodstone (component tier 5; 0.14 lb/unit; 582 gp/unit; catalyst; consumed); 1 × sparkling petal (component tier 1; 0.36 lb/unit; 10 gp/unit; material; consumed).

**Packaging:** no source vessels. Reserve 1 actual Glass vials for Standard output; 1 for Exceptional yield; 1 for full Masterwork yield. Each filled vial is 0.2 lb and one dose. At maximum yield with any eligible catalyst returned, reserve 0 lb additional clean carrier water. Owned intact spent vials may be reused; new ordinary Glass vials have a 1-gp reference price. All chosen-output packaging and carrier must be present before the check.

**Flawed:** {"mode": "half-fixed-duration", "durationSeconds": 14400, "instantCureUnchanged": false}. Exceptional/Masterwork choose finite yield or Standard quantity with every container at max/current HP 2, never both. No effect potency or extra cures.

**Provenance:** current effect and original ingredient identities are retained. Legacy fields remain in source/JSON and are inactive. No source deletion.

## recipe-234 — Mythic Stone Compress of Shamanic Bloodstone

**Source:** director-only; Herbalism level 16; tier 8; Very Rare; DC 22; 120 active hours; 1 doses. Standard batch reference 74659 gp.

**Preserved effect:** Applied over 1 minute, restores 6d6+8 hit points and treats one wound, burn, or infection appropriate to its ingredients.

**Operational effect:** After one uninterrupted active minute, attempt 6d6+8 ordinary magical nonspell HP healing under actual caps and blockers. After healing and its condition endpoints, choose at most one present local wound, burn, infection or Bleeding source appropriate to topical treatment. A Bleeding source with an existing Medicine-based removal DC permits one immediate WIS (Medicine) check against that DC using this dose as dressing, with no extra healer-kit charge. Do not attempt this if this dose already resolved a healing-triggered removal/treatment attempt for that record. Otherwise it supplies only one expressly required topical dressing/cleaning step in the source procedure; every other time, check, Supply, kit, medicine, rest and cure requirement remains. No defined interaction means no extra condition removal.

**Administration:** 1 uninterrupted active minute(s), requiring 10 consecutive regular-turn Actions in initiative and the full elapsed interval; keep touch and one hand available. Spend one actual dose at legal start. No benefit until completion; interruption does not refund it.

**Work:** Herbalist's Table; Herbalism kit, Mortar and pestle, Drying rack. Mode haven; field flag false; up to 2 assistants; formula required true.

**Exact ingredients:** 1 × Dried flowers (component tier 8; 0.1 lb/unit; 3000 gp/unit; substrate; consumed); 5 × Honey (component tier 8; 0.1 lb/unit; 3000 gp/unit; seasoning; consumed); 5 × Purified water (component tier 8; 0.5 lb/unit; 3000 gp/unit; solvent; consumed); 3 × Healing roots (component tier 8; 0.1 lb/unit; 3000 gp/unit; substrate; consumed); 4 × Crushed leaves (component tier 8; 0.1 lb/unit; 3000 gp/unit; ingredient; consumed); 1 × Mortar and pestle (component tier 8; 1.0 lb/unit; 9000 gp/unit; tool; returned); 1 × shamanic bloodstone (component tier 5; 0.14 lb/unit; 582 gp/unit; catalyst; consumed); 1 × sparkling petal (component tier 1; 0.36 lb/unit; 10 gp/unit; material; consumed).

**Packaging:** no source vessels. Reserve 1 actual Glass vials for Standard output; 1 for Exceptional yield; 1 for full Masterwork yield. Each filled vial is 0.2 lb and one dose. At maximum yield with any eligible catalyst returned, reserve 0 lb additional clean carrier water. Owned intact spent vials may be reused; new ordinary Glass vials have a 1-gp reference price. All chosen-output packaging and carrier must be present before the check.

**Flawed:** {"mode": "treat-as-Failed", "quantity": 0, "recovery": "framework 25 percent non-catalyst inputs"}. Exceptional/Masterwork choose finite yield or Standard quantity with every container at max/current HP 2, never both. No effect potency or extra cures.

**Provenance:** current effect and original ingredient identities are retained. Legacy fields remain in source/JSON and are inactive. No source deletion.

## recipe-235 — Ascendant Frost Remedy of Poisonous

**Source:** director-only; Herbalism level 18; tier 9; Very Rare; DC 22; 120 active hours; 1 doses. Standard batch reference 205983 gp.

**Preserved effect:** Grants +2 to saves and checks related to cold hazards for 8 hours.

**Operational effect:** Gain +2 on the recipient's own qualifying checks and saves against Cold hazards for 480 elapsed minutes. Saves against actual cold-damage or cold-exposure hazards; checks directly surviving or avoiding an actual cold hazard. No attack/damage bonus, automatic resistance, extra save or resource recovery.

**Administration:** Action, one available hand, drink or feed a compatible willing or Incapacitated recipient within 5 feet. Spend one actual dose at legal start. No benefit until completion; interruption does not refund it.

**Work:** Herbalist's Table; Herbalism kit, Mortar and pestle, Drying rack. Mode haven; field flag false; up to 2 assistants; formula required true.

**Exact ingredients:** 5 × Beeswax (component tier 9; 0.1 lb/unit; 7500 gp/unit; binder; consumed); 3 × Crushed leaves (component tier 9; 0.1 lb/unit; 7500 gp/unit; ingredient; consumed); 5 × Dried flowers (component tier 9; 0.1 lb/unit; 7500 gp/unit; substrate; consumed); 2 × Honey (component tier 9; 0.1 lb/unit; 7500 gp/unit; seasoning; consumed); 1 × Mortar and pestle (component tier 9; 1.0 lb/unit; 22500 gp/unit; tool; returned); 5 × Purified water (component tier 9; 0.5 lb/unit; 7500 gp/unit; solvent; consumed); 1 × alpha Poisonous trophy (component tier 5; 0.1 lb/unit; 557 gp/unit; catalyst; consumed); 1 × moonlight dust (component tier 5; 0.24 lb/unit; 1223 gp/unit; catalyst; consumed).

**Packaging:** no source vessels. Reserve 1 actual Glass vials for Standard output; 1 for Exceptional yield; 1 for full Masterwork yield. Each filled vial is 0.2 lb and one dose. At maximum yield with any eligible catalyst returned, reserve 0 lb additional clean carrier water. Owned intact spent vials may be reused; new ordinary Glass vials have a 1-gp reference price. All chosen-output packaging and carrier must be present before the check.

**Flawed:** {"mode": "half-fixed-duration", "durationSeconds": 14400, "instantCureUnchanged": false}. Exceptional/Masterwork choose finite yield or Standard quantity with every container at max/current HP 2, never both. No effect potency or extra cures.

**Provenance:** current effect and original ingredient identities are retained. Legacy fields remain in source/JSON and are inactive. No source deletion.

## recipe-236 — Ascendant Ember Powder of Shamanic Bloodstone

**Source:** director-only; Herbalism level 18; tier 9; Very Rare; DC 21; 120 active hours; 1 doses. Standard batch reference 129489 gp.

**Preserved effect:** Grants +2 to saves and checks related to fire hazards for 8 hours.

**Operational effect:** Gain +2 on the recipient's own qualifying checks and saves against Fire hazards for 480 elapsed minutes. Saves against actual fire-damage or fire environmental hazards; checks directly avoiding, extinguishing or safely traversing a fire hazard. No attack/damage bonus, automatic resistance, extra save or resource recovery.

**Administration:** Action, one available hand, drink or feed a compatible willing or Incapacitated recipient within 5 feet. Spend one actual dose at legal start. No benefit until completion; interruption does not refund it.

**Work:** Herbalist's Table; Herbalism kit, Mortar and pestle, Drying rack. Mode haven; field flag false; up to 2 assistants; formula required true.

**Exact ingredients:** 1 × Honey (component tier 9; 0.1 lb/unit; 7500 gp/unit; seasoning; consumed); 1 × Mortar and pestle (component tier 9; 1.0 lb/unit; 22500 gp/unit; tool; returned); 1 × Dried flowers (component tier 9; 0.1 lb/unit; 7500 gp/unit; substrate; consumed); 4 × Medicinal herbs (component tier 9; 0.1 lb/unit; 7500 gp/unit; substrate; consumed); 3 × Beeswax (component tier 9; 0.1 lb/unit; 7500 gp/unit; binder; consumed); 3 × Healing roots (component tier 9; 0.1 lb/unit; 7500 gp/unit; substrate; consumed); 1 × shamanic bloodstone (component tier 5; 0.14 lb/unit; 582 gp/unit; catalyst; consumed); 1 × worldroot bark (component tier 6; 0.13 lb/unit; 4536 gp/unit; material; consumed).

**Packaging:** no source vessels. Reserve 1 actual Glass vials for Standard output; 1 for Exceptional yield; 1 for full Masterwork yield. Each filled vial is 0.2 lb and one dose. At maximum yield with any eligible catalyst returned, reserve 0 lb additional clean carrier water. Owned intact spent vials may be reused; new ordinary Glass vials have a 1-gp reference price. All chosen-output packaging and carrier must be present before the check.

**Flawed:** {"mode": "half-fixed-duration", "durationSeconds": 14400, "instantCureUnchanged": false}. Exceptional/Masterwork choose finite yield or Standard quantity with every container at max/current HP 2, never both. No effect potency or extra cures.

**Provenance:** current effect and original ingredient identities are retained. Legacy fields remain in source/JSON and are inactive. No source deletion.

## recipe-237 — Transcendent Venom Balm of Poisonous

**Source:** director-only; Herbalism level 20; tier 10; Legendary; DC 25; 480 active hours; 1 doses. Standard batch reference 491641 gp.

**Preserved effect:** Applied over 1 minute, restores 8d6+10 hit points and treats one wound, burn, or infection appropriate to its ingredients.

**Operational effect:** After one uninterrupted active minute, attempt 8d6+10 ordinary magical nonspell HP healing under actual caps and blockers. After healing and its condition endpoints, choose at most one present local wound, burn, infection or Bleeding source appropriate to topical treatment. A Bleeding source with an existing Medicine-based removal DC permits one immediate WIS (Medicine) check against that DC using this dose as dressing, with no extra healer-kit charge. Do not attempt this if this dose already resolved a healing-triggered removal/treatment attempt for that record. Otherwise it supplies only one expressly required topical dressing/cleaning step in the source procedure; every other time, check, Supply, kit, medicine, rest and cure requirement remains. No defined interaction means no extra condition removal.

**Administration:** 1 uninterrupted active minute(s), requiring 10 consecutive regular-turn Actions in initiative and the full elapsed interval; keep touch and one hand available. Spend one actual dose at legal start. No benefit until completion; interruption does not refund it.

**Work:** Herbalist's Table; Herbalism kit, Mortar and pestle, Drying rack. Mode legacy; field flag false; up to 3 assistants; formula required true.

**Exact ingredients:** 1 × Mortar and pestle (component tier 10; 1.0 lb/unit; 54000 gp/unit; tool; returned); 4 × Dried flowers (component tier 10; 0.1 lb/unit; 18000 gp/unit; substrate; consumed); 4 × Medicinal herbs (component tier 10; 0.1 lb/unit; 18000 gp/unit; substrate; consumed); 4 × Natural oils (component tier 10; 0.5 lb/unit; 18000 gp/unit; solvent; consumed); 2 × Healing roots (component tier 10; 0.1 lb/unit; 18000 gp/unit; substrate; consumed); 5 × Beeswax (component tier 10; 0.1 lb/unit; 18000 gp/unit; binder; consumed); 1 × Crushed leaves (component tier 10; 0.1 lb/unit; 18000 gp/unit; ingredient; consumed); 1 × alpha Poisonous trophy (component tier 5; 0.1 lb/unit; 557 gp/unit; catalyst; consumed); 1 × Poisonous sinew (component tier 3; 0.38 lb/unit; 66 gp/unit; catalyst; consumed).

**Packaging:** no source vessels. Reserve 1 actual Glass vials for Standard output; 1 for Exceptional yield; 1 for full Masterwork yield. Each filled vial is 0.2 lb and one dose. At maximum yield with any eligible catalyst returned, reserve 0 lb additional clean carrier water. Owned intact spent vials may be reused; new ordinary Glass vials have a 1-gp reference price. All chosen-output packaging and carrier must be present before the check.

**Flawed:** {"mode": "treat-as-Failed", "quantity": 0, "recovery": "framework 25 percent non-catalyst inputs"}. Exceptional/Masterwork choose finite yield or Standard quantity with every container at max/current HP 2, never both. No effect potency or extra cures.

**Provenance:** current effect and original ingredient identities are retained. Legacy fields remain in source/JSON and are inactive. No source deletion.

## recipe-238 — Ascendant Grave Antidote of Shamanic Bloodstone

**Source:** director-only; Herbalism level 18; tier 9; Legendary; DC 23; 320 active hours; 1 doses. Standard batch reference 165722 gp.

**Preserved effect:** Ends the poisoned condition and grants advantage on saves against poison for until the next long rest.

**Operational effect:** End every present removable Poisoned application, without deleting its independent underlying cause; future exposure may reapply it. Gain advantage on saves against poison until the next completed beneficial Long Rest. No added numeric bonus, poison immunity, resistance, disease or intoxication cure.

**Administration:** Action, one available hand, drink or feed a compatible willing or Incapacitated recipient within 5 feet. Spend one actual dose at legal start. No benefit until completion; interruption does not refund it.

**Work:** Herbalist's Table; Herbalism kit, Mortar and pestle, Drying rack. Mode legacy; field flag false; up to 2 assistants; formula required true.

**Exact ingredients:** 5 × Beeswax (component tier 9; 0.1 lb/unit; 7500 gp/unit; binder; consumed); 1 × Mortar and pestle (component tier 9; 1.0 lb/unit; 22500 gp/unit; tool; returned); 1 × Crushed leaves (component tier 9; 0.1 lb/unit; 7500 gp/unit; ingredient; consumed); 1 × Healing roots (component tier 9; 0.1 lb/unit; 7500 gp/unit; substrate; consumed); 4 × Dried flowers (component tier 9; 0.1 lb/unit; 7500 gp/unit; substrate; consumed); 5 × Honey (component tier 9; 0.1 lb/unit; 7500 gp/unit; seasoning; consumed); 1 × shamanic bloodstone (component tier 5; 0.14 lb/unit; 582 gp/unit; catalyst; consumed); 1 × black blood sample (component tier 2; 0.38 lb/unit; 42 gp/unit; catalyst; consumed).

**Packaging:** no source vessels. Reserve 1 actual Glass vials for Standard output; 1 for Exceptional yield; 1 for full Masterwork yield. Each filled vial is 0.2 lb and one dose. At maximum yield with any eligible catalyst returned, reserve 0 lb additional clean carrier water. Owned intact spent vials may be reused; new ordinary Glass vials have a 1-gp reference price. All chosen-output packaging and carrier must be present before the check.

**Flawed:** {"mode": "treat-as-Failed", "quantity": 0, "recovery": "framework 25 percent non-catalyst inputs"}. Exceptional/Masterwork choose finite yield or Standard quantity with every container at max/current HP 2, never both. No effect potency or extra cures.

**Provenance:** current effect and original ingredient identities are retained. Legacy fields remain in source/JSON and are inactive. No source deletion.

## recipe-239 — Transcendent Mindward Powder of Caustic Goo

**Source:** director-only; Herbalism level 19; tier 10; Legendary; DC 24; 320 active hours; 1 doses. Standard batch reference 344136 gp.

**Preserved effect:** Grants +3 to saves and checks related to psychic hazards for until the next long rest.

**Operational effect:** Gain +3 on the recipient's own qualifying checks and saves against Psychic hazards until the next completed beneficial Long Rest. Actual psychic damage, mental intrusion or an explicitly psychic hazard; not every mental save or ordinary social influence. No attack/damage bonus, automatic resistance, extra save or resource recovery.

**Administration:** Action, one available hand, drink or feed a compatible willing or Incapacitated recipient within 5 feet. Spend one actual dose at legal start. No benefit until completion; interruption does not refund it.

**Work:** Herbalist's Table; Herbalism kit, Mortar and pestle, Drying rack. Mode legacy; field flag false; up to 2 assistants; formula required true.

**Exact ingredients:** 5 × Beeswax (component tier 10; 0.1 lb/unit; 18000 gp/unit; binder; consumed); 1 × Purified water (component tier 10; 0.5 lb/unit; 18000 gp/unit; solvent; consumed); 1 × Mortar and pestle (component tier 10; 1.0 lb/unit; 54000 gp/unit; tool; returned); 4 × Natural oils (component tier 10; 0.5 lb/unit; 18000 gp/unit; solvent; consumed); 4 × Healing roots (component tier 10; 0.1 lb/unit; 18000 gp/unit; substrate; consumed); 1 × caustic goo (component tier 1; 0.99 lb/unit; 8 gp/unit; material; consumed); 1 × blighted bark (component tier 5; 0.26 lb/unit; 656 gp/unit; material; consumed).

**Packaging:** no source vessels. Reserve 1 actual Glass vials for Standard output; 1 for Exceptional yield; 1 for full Masterwork yield. Each filled vial is 0.2 lb and one dose. At maximum yield with any eligible catalyst returned, reserve 0 lb additional clean carrier water. Owned intact spent vials may be reused; new ordinary Glass vials have a 1-gp reference price. All chosen-output packaging and carrier must be present before the check.

**Flawed:** {"mode": "treat-as-Failed", "quantity": 0, "recovery": "framework 25 percent non-catalyst inputs"}. Exceptional/Masterwork choose finite yield or Standard quantity with every container at max/current HP 2, never both. No effect potency or extra cures.

**Provenance:** current effect and original ingredient identities are retained. Legacy fields remain in source/JSON and are inactive. No source deletion.

## recipe-240 — Transcendent Storm Balm of Sparkling Petal

**Source:** director-only; Herbalism level 20; tier 10; Mythic; DC 28; 960 active hours; 1 doses. Standard batch reference 454023 gp.

**Preserved effect:** Applied over 1 minute, restores 10d6+12 hit points and treats one wound, burn, or infection appropriate to its ingredients.

**Operational effect:** After one uninterrupted active minute, attempt 10d6+12 ordinary magical nonspell HP healing under actual caps and blockers. After healing and its condition endpoints, choose at most one present local wound, burn, infection or Bleeding source appropriate to topical treatment. A Bleeding source with an existing Medicine-based removal DC permits one immediate WIS (Medicine) check against that DC using this dose as dressing, with no extra healer-kit charge. Do not attempt this if this dose already resolved a healing-triggered removal/treatment attempt for that record. Otherwise it supplies only one expressly required topical dressing/cleaning step in the source procedure; every other time, check, Supply, kit, medicine, rest and cure requirement remains. No defined interaction means no extra condition removal.

**Administration:** 1 uninterrupted active minute(s), requiring 10 consecutive regular-turn Actions in initiative and the full elapsed interval; keep touch and one hand available. Spend one actual dose at legal start. No benefit until completion; interruption does not refund it.

**Work:** Herbalist's Table; Herbalism kit, Mortar and pestle, Drying rack. Mode legacy; field flag false; up to 3 assistants; formula required true.

**Exact ingredients:** 4 × Crushed leaves (component tier 10; 0.1 lb/unit; 18000 gp/unit; ingredient; consumed); 1 × Mortar and pestle (component tier 10; 1.0 lb/unit; 54000 gp/unit; tool; returned); 4 × Medicinal herbs (component tier 10; 0.1 lb/unit; 18000 gp/unit; substrate; consumed); 5 × Beeswax (component tier 10; 0.1 lb/unit; 18000 gp/unit; binder; consumed); 1 × Purified water (component tier 10; 0.5 lb/unit; 18000 gp/unit; solvent; consumed); 4 × Honey (component tier 10; 0.1 lb/unit; 18000 gp/unit; seasoning; consumed); 1 × sparkling petal (component tier 1; 0.36 lb/unit; 10 gp/unit; material; consumed); 1 × worldroot bark (component tier 6; 0.13 lb/unit; 4536 gp/unit; material; consumed); 1 × blighted bark (component tier 5; 0.26 lb/unit; 656 gp/unit; material; consumed).

**Packaging:** no source vessels. Reserve 1 actual Glass vials for Standard output; 1 for Exceptional yield; 1 for full Masterwork yield. Each filled vial is 0.2 lb and one dose. At maximum yield with any eligible catalyst returned, reserve 0 lb additional clean carrier water. Owned intact spent vials may be reused; new ordinary Glass vials have a 1-gp reference price. All chosen-output packaging and carrier must be present before the check.

**Flawed:** {"mode": "treat-as-Failed", "quantity": 0, "recovery": "framework 25 percent non-catalyst inputs"}. Exceptional/Masterwork choose finite yield or Standard quantity with every container at max/current HP 2, never both. No effect potency or extra cures.

**Provenance:** current effect and original ingredient identities are retained. Legacy fields remain in source/JSON and are inactive. No source deletion.

## recipe-644 — Dream-Bark Sleeping Draught

**Source:** public; Herbalism level 5; tier 3; Uncommon; DC 13; 8 active hours; 1 doses. Standard batch reference 179 gp.

**Preserved effect:** Grants +1 to saves and checks related to psychic hazards for 1 hour.

**Operational effect:** Gain +1 on the recipient's own qualifying checks and saves against Psychic hazards for 60 elapsed minutes. Actual psychic damage, mental intrusion or an explicitly psychic hazard; not every mental save or ordinary social influence. No attack/damage bonus, automatic resistance, extra save or resource recovery.

**Administration:** Action, one available hand, drink or feed a compatible willing or Incapacitated recipient within 5 feet. Spend one actual dose at legal start. No benefit until completion; interruption does not refund it.

**Work:** Herbalist's Table; Herbalism kit, Mortar and pestle, Drying rack. Mode expedition; field flag true; up to 0 assistants; formula required true.

**Exact ingredients:** 1 × dream bark (component tier 2; 0.45 lb/unit; 31 gp/unit; material; consumed); 1 × Purified water (component tier 3; 0.5 lb/unit; 25 gp/unit; solvent; consumed); 1 × Dried flowers (component tier 3; 0.1 lb/unit; 25 gp/unit; substrate; consumed); 1 × Honey (component tier 3; 0.1 lb/unit; 25 gp/unit; seasoning; consumed).

**Packaging:** no source vessels. Reserve 1 actual Glass vials for Standard output; 1 for Exceptional yield; 1 for full Masterwork yield. Each filled vial is 0.2 lb and one dose. At maximum yield with any eligible catalyst returned, reserve 0 lb additional clean carrier water. Owned intact spent vials may be reused; new ordinary Glass vials have a 1-gp reference price. All chosen-output packaging and carrier must be present before the check.

**Flawed:** {"mode": "half-fixed-duration", "durationSeconds": 1800, "instantCureUnchanged": false}. Exceptional/Masterwork choose finite yield or Standard quantity with every container at max/current HP 2, never both. No effect potency or extra cures.

**Provenance:** current effect and original ingredient identities are retained. Legacy fields remain in source/JSON and are inactive. No source deletion.

## recipe-645 — Living-Root Regeneration Poultice

**Source:** public; Herbalism level 2; tier 1; Common; DC 10; 2 active hours; 1 doses. Standard batch reference 29 gp.

**Preserved effect:** Applied over 1 minute, restores 1d6+2 hit points and treats one wound, burn, or infection appropriate to its ingredients.

**Operational effect:** After one uninterrupted active minute, attempt 1d6+2 ordinary magical nonspell HP healing under actual caps and blockers. After healing and its condition endpoints, choose at most one present local wound, burn, infection or Bleeding source appropriate to topical treatment. A Bleeding source with an existing Medicine-based removal DC permits one immediate WIS (Medicine) check against that DC using this dose as dressing, with no extra healer-kit charge. Do not attempt this if this dose already resolved a healing-triggered removal/treatment attempt for that record. Otherwise it supplies only one expressly required topical dressing/cleaning step in the source procedure; every other time, check, Supply, kit, medicine, rest and cure requirement remains. No defined interaction means no extra condition removal.

**Administration:** 1 uninterrupted active minute(s), requiring 10 consecutive regular-turn Actions in initiative and the full elapsed interval; keep touch and one hand available. Spend one actual dose at legal start. No benefit until completion; interruption does not refund it.

**Work:** Herbalist's Table; Herbalism kit, Mortar and pestle, Drying rack. Mode field; field flag true; up to 0 assistants; formula required false.

**Exact ingredients:** 1 × living root (component tier 1; 0.29 lb/unit; 12 gp/unit; material; consumed); 1 × Beeswax (component tier 1; 0.1 lb/unit; 2 gp/unit; binder; consumed); 1 × Natural oils (component tier 1; 0.5 lb/unit; 2 gp/unit; solvent; consumed); 1 × Medicinal herbs (component tier 1; 0.1 lb/unit; 2 gp/unit; substrate; consumed).

**Packaging:** no source vessels. Reserve 1 actual Glass vials for Standard output; 1 for Exceptional yield; 1 for full Masterwork yield. Each filled vial is 0.2 lb and one dose. At maximum yield with any eligible catalyst returned, reserve 0 lb additional clean carrier water. Owned intact spent vials may be reused; new ordinary Glass vials have a 1-gp reference price. All chosen-output packaging and carrier must be present before the check.

**Flawed:** {"mode": "treat-as-Failed", "quantity": 0, "recovery": "framework 25 percent non-catalyst inputs"}. Exceptional/Masterwork choose finite yield or Standard quantity with every container at max/current HP 2, never both. No effect potency or extra cures.

**Provenance:** current effect and original ingredient identities are retained. Legacy fields remain in source/JSON and are inactive. No source deletion.

## recipe-646 — Blighted-Bark Rotbane

**Source:** director-only; Herbalism level 16; tier 9; Legendary; DC 24; 160 active hours; 1 doses. Standard batch reference 36044 gp.

**Preserved effect:** Ends the poisoned condition and grants advantage on saves against poison for until the next long rest.

**Operational effect:** End every present removable Poisoned application, without deleting its independent underlying cause; future exposure may reapply it. Gain advantage on saves against poison until the next completed beneficial Long Rest. No added numeric bonus, poison immunity, resistance, disease or intoxication cure.

**Administration:** Action, one available hand, drink or feed a compatible willing or Incapacitated recipient within 5 feet. Spend one actual dose at legal start. No benefit until completion; interruption does not refund it.

**Work:** Herbalist's Table; Herbalism kit, Mortar and pestle, Drying rack. Mode haven; field flag false; up to 2 assistants; formula required true.

**Exact ingredients:** 1 × blighted bark (component tier 5; 0.26 lb/unit; 656 gp/unit; material; consumed); 1 × foul dust (component tier 2; 0.6 lb/unit; 20 gp/unit; material; consumed); 1 × Purified water (component tier 9; 0.5 lb/unit; 7500 gp/unit; solvent; consumed); 1 × Healing roots (component tier 9; 0.1 lb/unit; 7500 gp/unit; substrate; consumed); 1 × Honey (component tier 9; 0.1 lb/unit; 7500 gp/unit; seasoning; consumed).

**Packaging:** no source vessels. Reserve 1 actual Glass vials for Standard output; 1 for Exceptional yield; 1 for full Masterwork yield. Each filled vial is 0.2 lb and one dose. At maximum yield with any eligible catalyst returned, reserve 0 lb additional clean carrier water. Owned intact spent vials may be reused; new ordinary Glass vials have a 1-gp reference price. All chosen-output packaging and carrier must be present before the check.

**Flawed:** {"mode": "treat-as-Failed", "quantity": 0, "recovery": "framework 25 percent non-catalyst inputs"}. Exceptional/Masterwork choose finite yield or Standard quantity with every container at max/current HP 2, never both. No effect potency or extra cures.

**Provenance:** current effect and original ingredient identities are retained. Legacy fields remain in source/JSON and are inactive. No source deletion.

## recipe-647 — Worldroot Panacea

**Source:** director-only; Herbalism level 20; tier 10; Mythic; DC 28; 480 active hours; 1 doses. Standard batch reference 98826 gp.

**Preserved effect:** Applied over 10 minutes, ends one disease, poison, curse, or exhaustion level and restores 10d6+20 hit points. A creature can benefit only once per season.

**Operational effect:** Apply over 10 uninterrupted active minutes. On completion, end one present eligible disease, poison/toxin or external curse source, or remove one legally removable Exhaustion level; then attempt 10d6+20 ordinary magical nonspell HP healing. Cure and healing are independent. Use the Director procedure for the recipient season limit, successful-benefit commitment, concurrent-attempt lock and actual source restrictions. No Wound, intrinsic trait, Corruption or resurrection removal.

**Administration:** 10 uninterrupted active minute(s), requiring 100 consecutive regular-turn Actions in initiative and the full elapsed interval; keep touch and one hand available. Spend one actual dose at legal start. No benefit until completion; interruption does not refund it.

**Work:** Herbalist's Table; Herbalism kit, Mortar and pestle, Drying rack. Mode legacy; field flag false; up to 3 assistants; formula required true.

**Exact ingredients:** 1 × worldroot bark (component tier 6; 0.13 lb/unit; 4536 gp/unit; material; consumed); 1 × ancient growth essence (component tier 6; 0.15 lb/unit; 4148 gp/unit; material; consumed); 1 × Purified water (component tier 10; 0.5 lb/unit; 18000 gp/unit; solvent; consumed); 1 × Beeswax (component tier 10; 0.1 lb/unit; 18000 gp/unit; binder; consumed); 1 × Medicinal herbs (component tier 10; 0.1 lb/unit; 18000 gp/unit; substrate; consumed).

**Packaging:** no source vessels. Reserve 1 actual Glass vials for Standard output; 1 for Exceptional yield; 1 for full Masterwork yield. Each filled vial is 0.2 lb and one dose. At maximum yield with any eligible catalyst returned, reserve 0 lb additional clean carrier water. Owned intact spent vials may be reused; new ordinary Glass vials have a 1-gp reference price. All chosen-output packaging and carrier must be present before the check.

**Flawed:** {"mode": "treat-as-Failed", "quantity": 0, "recovery": "framework 25 percent non-catalyst inputs"}. Exceptional/Masterwork choose finite yield or Standard quantity with every container at max/current HP 2, never both. No effect potency or extra cures.

**Provenance:** current effect and original ingredient identities are retained. Legacy fields remain in source/JSON and are inactive. No source deletion.

**Director procedure:** [Panacea recipient limit and cure order](HERBALISM_INTERNAL_PROCEDURES.md).
